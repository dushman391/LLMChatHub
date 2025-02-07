# LLMChatHub 🤖💬

This project leverages multiple AI models to create an interactive chatbot experience. Users can bring their own models and have conversations without risking their data leaving their premises/devices. 🚀

## Features ✨
- **Multiple AI Models**: Choose from various models like `llama3.2`, `phi4:latest`, `qwen:14b`, `qwen2:7b`, and `gemma2:9b`.
- **Azure OpenAI Integration**: Option to use Azure OpenAI for generating responses.
- **Conversation History**: Save and load conversation history.
- **Interactive UI**: Built with Gradio for a user-friendly interface.
- **Model Status**: Check the status of installed models and get commands to install missing models.

## Getting Started 🛠️

### Prerequisites 📋
- Python 3.7+
- Install required packages:
    ```sh
    pip install -r requirements.txt
    ```
- Ollama installed
- A server with sufficient compute resources to run the selected models

### Running the Project ▶️
Start the server:
```sh
python app.py
```
Access the UI: Open your browser and go to `http://localhost:7860`.

### Usage 📝
- **Choose a Model**: Select a model from the dropdown menu.
- **Type Your Message**: Enter your message in the textbox and hit enter.
- **View Responses**: The chatbot will respond using the selected model.
- **Switch Models Mid-Conversation**: Select a different model at any time, and the conversation history will be seamlessly transferred to the new model.
- **Save Conversations**: Click the "Save Conversation" button to save the chat history.
- **Load Conversations**: Use the dropdown to select and load previous conversations.
- **Adding New models**: Go to models_config.py and add the model id from Ollama Model Library. Rerun the app.py, click on "Model Status" and hit refresh. 

### Environment Variables 🌐
- `AZURE_OPENAI_ENDPOINT`: Your Azure OpenAI endpoint.
- `AZURE_OPENAI_API_KEY`: Your Azure OpenAI API key.


## License 📄
This project is licensed under the Apache License 2.0. See the LICENSE file for details.

## Contributing 🤝
Feel free to fork this project, submit issues, and send pull requests. Contributions are welcome! 🎉

## Acknowledgements 🙏
Thanks to the creators of the AI models and Gradio for making this project possible.

Enjoy chatting! 💬✨