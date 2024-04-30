# Python Client for the Liquid API

## 📦 Installation
```bash
pip install -U liquidai
```

## API Key

To accesss the following URLs, you need to create an API key at labs.liquid.ai with your account.
You can find your API key in the profile tab of the Liquid platform (left bottom icon in the navigation bar).

## OpenAI compatible API
For openai and langchain compatible [api documentation](https://github.com/Liquid4All/liquid_client/blob/main/openai-api.md).

- `/chat/completions` endpoint example notebooks: 
    - [Openai Client](https://github.com/Liquid4All/liquid_client/tree/main/examples/openai/chat_completion.ipynb)
    - [Langchain Client](https://github.com/Liquid4All/liquid_client/tree/main/examples/langchain/chat_openai.ipynb)

- `/embeddings`

## 💬 Other liquid api endpoints
- `/complete`. Retrieval augmentation enabled completion endpoint, can be passed with files.

You need to set the environment variables `LIQUID_URL` and `LIQUID_API_KEY` to the UR and your API key of your Liquid AI subscription respectively.

🔐 **API Keys** The most secure way is to set the environment variables, which the Liquid client will automatically use.
```bash
export LIQUID_URL="https://labs.liquid.ai/api/v1"
export LIQUID_API_KEY="9cba1....."
```

Alternatively, you can also pass the `base_url` and `api_key` parameters to the `Client` constructor.
```python
from liquidai import Client
# Create a client object with the API URL and API key
client = Client()
print("Models: ", client.list_models()) # List all models
# Create a conversation with the model (a list of messages)
chat = [{"role": "user", "content": "Hello world in python!"}]
response = client.complete(chat)
print(f"Response: {response['message']['content']}")
```
Output:
```
>>> Models:  ['liquid-preview-0.1']
>>> Response: Here is how to code a Hello World program in Python: print("Hello, world!")
```

Multi-turn conversations:
```python
chat.append(response["message"]) # add assistant message to conversation
chat.append({"role": "user", "content": "And in C++?"})
response = client.complete(chat)
print(f"Response: {response['message']['content']}")
```

Output:
```
>>> #include <iostream>
>>> 
>>> int main() {
>>>     std::cout << "Hello, World!" << std::endl;
>>>     return 0;
>>> }
```

## 📚 Adding Knowledge Bases to the Model
```python
# Let's create an example knowledge base
test_file = "test.txt"
with open(test_file, "w") as f:
    f.write("The name of the CEO of Liquid is Ramin Hasani.")
# Upload the file to the server
response = client.upload_file(test_file)
print(f"Uploaded {test_file} to {response['filename']}")
files = client.list_files()
print(f"Files: {files}")
```

Output:
```
>>> Uploaded test.txt to text.txt
>>> Files: ['text.txt']
```

Next we can tell the model to use the document we just uploaded:

```python
chat = [
    {"role": "user", "content": "Who is the CEO of Liquid?", "files": ["test.txt"]}
]
response = client.complete(chat)
print(f"Response: {response['message']['content']}")
```
Output:
```
>>> Response: The CEO of Liquid is Ramin Hasani.
```

**Removing files:** Finally we can delete the file from the server:

```python
client.delete_file(test_file)
print(f"Deleted {test_file}")

files = client.list_files()
print(f"Files: {files}")
```
Output:
```
>>> Deleted test.txt
>>> Files: []
```

## 📌 Full Examples

- [Quickstart](https://github.com/Liquid4All/liquid_client/tree/main/examples/liquid_api.ipynb) Full example of the basic usage described above.
- [AI2 Reasoning Challenge](https://github.com/Liquid4All/liquid_client/tree/main/examples/evals/run_ai2rc.py) Runs the AI2 Reasoning Challenge via the Liquid platform.
- [Code clone detection benchmark](https://github.com/Liquid4All/liquid_client/blob/main/examples/evals/code_clone_detection.py) Runs part of the Codegluex code clone detection benchmark
- [Upload multiple files](https://github.com/Liquid4All/liquid_client/tree/main/examples/upload_folder.py) Script to upload a folder of files to the Liquid platform.

