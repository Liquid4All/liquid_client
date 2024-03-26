import liquidai
import os

"""
This example is used to test https://labs.liquid.ai with the API versioning string as api/v1/. Switch branch `git branch api-v1` before proceeding.

Add environment variables
```bash
export LIQUID_URL="https://labs.liquid.ai"
export LIQUID_API_KEY="9cba1....."
```
"""


def get_completion(client):
    chat = [{"role": "user", "content": "what is the largest animal on earth?"}]
    response = client.complete(chat)
    print(f"Response: {response['message']['content']}")


def test_rag_source(client):
    test_file = "test.txt"
    with open(test_file, "w") as f:
        f.write("The name of the CEO of Liquid is Ramin Hasani.")
    db_document = client.upload_file(test_file)
    print(f"Uploaded {test_file} to {db_document['name']}")
    files = client.list_files()
    print(f"Files: {files}")
    chat = [{"role": "user", "content": "Who is the CEO of Liquid?", "files": ["test.txt"]}]
    response = client.complete(chat)
    print(f"Response: {response['message']['content']}")

    # Delete the fil in db
    client.delete_file(test_file)
    print(f"Deleted {test_file}")
    files = client.list_files()
    print(f"Files: {files}")

    # Delete the file locally
    os.remove(test_file)
    print(f"Deleted {test_file} locally")


def test_coding(client):
    chat = [{"role": "user", "content": "write binary search in python"}]
    response = client.complete(chat)
    print(f"Response: {response['message']['content']}")


if __name__ == "__main__":
    # Don't forget to set the LIQUID_URL and LIQUID_API_KEY environment variable
    client = liquidai.Client()
    print("Models: ", client.list_models())
    get_completion(client)
    test_rag_source(client)
    test_coding(client)