import os
from langchain_openai import AzureChatOpenAI
import json
import gradio as gr
import requests
from datetime import datetime
import subprocess
from models_config import models  # Import the model list

def get_azure_model():
    azure_url = os.getenv("AZURE_OPENAI_ENDPOINT")
    azure_key = os.getenv("AZURE_OPENAI_API_KEY")
    if not azure_url or not azure_key:
        print("Azure OpenAI credentials are not set. Skipping Azure model initialization.")
        return None
    env = '[{"model": "gpt4","base_url": "'+ azure_url +'","api_key": "'+ azure_key +'", "api_type": "azure", "api_version": "2024-02-15-preview"}]'
    os.environ["KAIT_OPENAI_KEY"] = env
    return AzureChatOpenAI(
        openai_api_version="2023-06-01-preview",
        azure_deployment="gpt4",
        azure_api_key=azure_key,
        azure_base_url=azure_url
    )

def ollama_model_invoke(prompt, model_name):
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    data = {"model": model_name, "prompt": prompt, "stream": False}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        response_text = response.text
        data = json.loads(response_text)
        actual_response = data['response']
        return actual_response
    else:
        return f"Error: {response.status_code} {response.text}"

# Global variable to store conversation history
conversation_history = []
loaded_filename = None

def generate_conversation_name(conversation_history):
    prompt = "\n".join([f"{role}: {message}" for role, message in conversation_history]) + "\nGenerate a very simple and meaningful name for this conversation. Maximum 3 words. Do not include anything else in the response."
    response = ollama_model_invoke(prompt, "llama3.2")
    return response.strip()

def save_conversation(filename=None):
    global conversation_history
    if filename is None:
        conversation_name = generate_conversation_name(conversation_history)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{conversation_name} - {timestamp}.json"
    with open(filename, 'w') as file:
        json.dump(conversation_history, file)
    return conversation_history  # Return the conversation history instead of the filename

def load_conversation(filename):
    global conversation_history, loaded_filename
    with open(filename, 'r') as file:
        conversation_history = json.load(file)
    loaded_filename = filename
    return conversation_history

def handle_user_input(user_question, model_choice):
    global conversation_history
    if not model_choice:
        return [("Error", "Model choice is not selected.")]
    conversation_history.append(("User", user_question))
    prompt = "\n".join([f"{role}: {message}" for role, message in conversation_history]) + "\nAI:"
    if model_choice == "AzureOpen AI":
        azure_model = get_azure_model()
        if azure_model is None:
            return [("Error", "Azure OpenAI credentials are not set.")]
        response = azure_model.invoke(prompt).content
    else:
        response = ollama_model_invoke(prompt, model_choice.split()[1])
    conversation_history.append((f"AI ({model_choice})", response))
    return conversation_history

def clear_conversation():
    global conversation_history
    conversation_history = []
    return conversation_history

def get_saved_conversations():
    return [f for f in os.listdir() if f.endswith('.json')]

def get_installed_models():
    try:
        output = subprocess.check_output(['ollama', 'list'], text=True)
        lines = output.strip().split('\n')
        installed_models = [line.split()[0] for line in lines[1:]]  # Skip the header and get the first column
        return installed_models
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output}"

def check_model_status():
    installed_models = get_installed_models()
    if isinstance(installed_models, str):
        return installed_models  # Return error message if any
    missing_models = [model for model in models if model not in installed_models]
    status = f"Installed Models: {', '.join(installed_models)}\n"
    if missing_models:
        status += f"Missing Models: {', '.join(missing_models)}\n"
        status += "Please install the missing models using the following commands:\n"
        for model in missing_models:
            status += f"ollama run {model}\n"
    else:
        status += "All models are installed."
    return status

if __name__ == '__main__':
    with gr.Blocks() as demo:
        with gr.Tabs():
            with gr.TabItem("Chat"):
                model_choice = gr.Dropdown(choices=["AzureOpen AI"] + [f"Ollama {model}" for model in models], label="Choose Model", value=None)
                chatbot = gr.Chatbot()
                user_input = gr.Textbox(placeholder="Type your message here...")
                clear_button = gr.Button("Clear")
                save_button = gr.Button("Save Conversation")
                load_dropdown = gr.Dropdown(choices=get_saved_conversations(), label="Load Conversation")
                load_button = gr.Button("Load")

                user_input.submit(handle_user_input, inputs=[user_input, model_choice], outputs=chatbot)
                clear_button.click(clear_conversation, None, chatbot)
                save_button.click(lambda: save_conversation(loaded_filename), None, chatbot)
                load_button.click(load_conversation, inputs=[load_dropdown], outputs=chatbot)

            with gr.TabItem("Model Status"):
                model_status = gr.Textbox(label="Model Status", interactive=False)
                refresh_button = gr.Button("Refresh")

                refresh_button.click(lambda: check_model_status(), None, model_status)

    demo.launch()
