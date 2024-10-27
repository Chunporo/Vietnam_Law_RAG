from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)

CHAT_HISTORY_FILE = 'chat_history.json'

# Function to ensure chat history file exists with valid JSON
def ensure_chat_history_file():
    if not os.path.exists(CHAT_HISTORY_FILE):
        print("Chat history file does not exist. Creating a new one.")
        with open(CHAT_HISTORY_FILE, 'w', encoding='utf-8') as file:
            json.dump([], file) 
    else:
        # Check if the file has valid JSON, otherwise reset it
        try:
            with open(CHAT_HISTORY_FILE, 'r', encoding='utf-8') as file:
                json.load(file)
        except json.JSONDecodeError:
            print("Chat history file is corrupted. Resetting it.")
            with open(CHAT_HISTORY_FILE, 'w', encoding='utf-8') as file:
                json.dump([], file)

# Function to save chat history to JSON file
def save_chat_history(user_input, system_output):
    ensure_chat_history_file()  # Ensure the file exists before saving

    chat_entry = {"user": user_input, "system": system_output}
    with open(CHAT_HISTORY_FILE, 'r', encoding='utf-8') as file:
        chat_history = json.load(file)

    chat_history.append(chat_entry)
    with open(CHAT_HISTORY_FILE, 'w', encoding='utf-8') as file:
        json.dump(chat_history, file, ensure_ascii=False, indent=4)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_question = request.form['question']
        
        # Placeholder response from the RAG system
        system_response = "This is a placeholder answer from the RAG system."
        
        # Save chat history
        save_chat_history(user_question, system_response)
        
        return render_template('index.html', user_question=user_question, system_response=system_response)
    
    return render_template('index.html')

@app.route('/history')
def history():
    ensure_chat_history_file()  # Ensure the file exists before loading

    with open(CHAT_HISTORY_FILE, 'r', encoding='utf-8') as file:
        chat_history = json.load(file)
    
    return render_template('history.html', chat_history=chat_history)

if __name__ == '__main__':
    app.run(debug=True)
