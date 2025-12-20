# Week 1 - Day 2: Additional Exercises
#
# Welcome to the practice exercises for the concepts covered in Day 2. 
# These tasks are designed to solidify your understanding of API endpoints, 
# client libraries, and the power of local models.
#
# To run this file, you can execute it from your terminal:
# python week1/week1_day2_exercises.py
#
# Or you can copy and paste each exercise into a new, clean Jupyter Notebook cell.

import os
from dotenv import load_dotenv
from openai import OpenAI
import requests
import json

# --- Pre-requisites & Setup ---
print("--- Setting up clients ---")
# Load environment variables
load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')

# Initialize the OpenAI client for OpenAI services
if not api_key:
    print("OpenAI API key not found. Skipping OpenAI client setup.")
    openai_client = None
else:
    openai_client = OpenAI()
    print("OpenAI client set up.")

# Initialize a client for Ollama
try:
    ollama_client = OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama" # required, but can be any string
    )
    # Check if Ollama is running
    ollama_client.models.list()
    print("Ollama client set up.")
except Exception as e:
    print("Could not connect to Ollama. Please ensure it is running.")
    print("You can start it by running 'ollama serve' in your terminal.")
    ollama_client = None

print("Setup complete.\n")


# --- Exercise 1: The Manual API Call ---
def exercise_1():
    print("\n--- Exercise 1: The Manual API Call ---")
    if not openai_client:
        print("OpenAI client not available. Skipping exercise.")
        return

    openai_endpoint = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-5-nano",
        "messages": [
            {"role": "system", "content": "You are a world-class historian with a knack for finding fascinating, little-known facts."},
            {"role": "user", "content": "Tell me a surprising fun fact about the Roman Empire."}
        ]
    }
    
    print("Making manual POST request to OpenAI...")
    try:
        response = requests.post(openai_endpoint, headers=headers, json=payload)
        if response.status_code == 200:
            response_data = response.json()
            content = response_data['choices'][0]['message']['content']
            print("SUCCESS! Response from API:")
            print(content)
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"An error occurred: {e}")

# --- Exercise 2: The Local Poet ---
def exercise_2():
    print("\n--- Exercise 2: The Local Poet ---")
    if not ollama_client:
        print("Ollama client not available. Skipping exercise.")
        return

    system_prompt = "You are a poet who finds beauty in technology and logic."
    user_prompt = "Write a four-line poem about the elegance and beauty of writing code." 
    
    print("Asking local model 'phi3' to write a poem...")
    try:
        response = ollama_client.chat.completions.create(
            model="phi3",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        print("SUCCESS! Response from model:")
        print(response.choices[0].message.content)
    except Exception as e:
        print("Could not connect to Ollama. Please ensure it is running.")
        print("You can start it by running 'ollama serve' in your terminal.")
        print(f"An error occurred. Have you pulled the 'phi3' model? (ollama pull phi3)")
        print(e)


# --- Exercise 3: The Model Comparator ---
def exercise_3():
    print("\n--- Exercise 3: The Model Comparator ---")
    if not ollama_client:
        print("Ollama client not available. Skipping exercise.")
        return

    def ask_local_model(model_name, question):
        try:
            response = ollama_client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": question}]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error with model {model_name}: {e}"

    question_to_ask = "What is the most important skill for a software engineer in the age of AI?"
    
    print(f"Asking llama3.2: '{question_to_ask}'")
    llama_answer = ask_local_model("llama3.2", question_to_ask)
    print("--- Answer from llama3.2 ---")
    print(llama_answer)
    
    print(f"\nAsking phi3: '{question_to_ask}'")
    phi_answer = ask_local_model("phi3", question_to_ask)
    print("--- Answer from phi3 ---")
    print(phi_answer)


# --- Exercise 4: The Web Summarizer, Re-routed ---
def exercise_4():
    print("\n--- Exercise 4: The Web Summarizer, Re-routed ---")
    if not ollama_client:
        print("Ollama client not available. Skipping exercise.")
        return
        
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        print("BeautifulSoup4 is not installed. Please run 'pip install beautifulsoup4'.")
        return

    def fetch_website_contents(url):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            for script_or_style in soup(['script', 'style']):
                script_or_style.decompose()
            return " ".join(t for t in soup.stripped_strings)
        except requests.exceptions.RequestException as e:
            return f"Error fetching website: {e}"

    def summarize_with_ollama(url):
        print(f"Fetching content from {url}...")
        website_content = fetch_website_contents(url)
        if website_content.startswith("Error"):
            return website_content
        
        print("Content fetched. Summarizing with llama3.2...")
        system_prompt = "You are an expert summarizer. Create a concise, easy-to-read summary of the following web content."
        user_prompt = f"Please summarize this content: \n\n{website_content[:4000]}"

        try:
            response = ollama_client.chat.completions.create(
                model="llama3.2",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error summarizing: {e}"

    summary = summarize_with_ollama("https://www.theverge.com/")
    print("\n--- SUMMARY ---")
    print(summary)


# --- Main execution block ---
if __name__ == "__main__":
    exercise_1()
    exercise_2()
    exercise_3()
    exercise_4()
