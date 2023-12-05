# Python Client for the Liquid API

## 📦 Installation
```bash
pip install -U liquidai
```

## 💬 Basic Usage

To access the API you need to set the environment variables `LIQUID_URL` and `LIQUID_API_KEY` to the UR and your API key of your Liquid AI subscription respectively.
You can find your API key in the My Account page of the Liquid platform (left bottom icon in the navigation bar).

🔐 **API Keys** The most secure way to set the environment variables, which the Liquid client will automatically use.
```bash
export LIQUID_URL="http://127.0.0.1:5000"
export LIQUID_API_KEY="9cba10db38d29db7b9f03503ef46146c1a431275d05c5c9a2fd278308c0d785d"
```

Alternatively, you can also pass the `api_url` and `api_key` parameters to the `Client` constructor.
```python
# Create a client object with the API URL and API key
client = Client()
print("Models: ", client.list_models()) # List all models
# Create a conversation with the model (a list of messages)
chat = [{"role": "user", "content": "Hello, world!"}]
response = client.complete(chat)
print(f"Response: {response['message']['content']}")
```
Output:
```
>>> Models:  ['liquid0']
>>> Response: Here is how to code a Hello World program in Python: print("Hello, world!")
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

- [Quickstart](https://github.com/Liquid4All/liquid_client/tree/main/examples/hello_world.py) Full example of the basic usage described above.
- [AI2 Reasoning Challenge](https://github.com/Liquid4All/liquid_client/tree/main/examples/run_ai2rc.py) Runs the AI2 Reasoning Challenge via the Liquid platform.
- [Upload multiple files](https://github.com/Liquid4All/liquid_client/tree/main/examples/upload_folder.py) Script to upload a folder of files to the Liquid platform.

