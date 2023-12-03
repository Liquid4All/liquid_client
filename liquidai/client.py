import httpx
import os
import json


class Client:
    def __init__(self, base_url, api_key=None):
        self.base_url = base_url
        if api_key is None:
            if "LIQUID_API_KEY" not in os.environ:
                raise ValueError(
                    "API key not found. Please set LIQUID_API_KEY environment variable"
                )
            api_key = os.environ["LIQUID_API_KEY"]
        self.api_key = api_key
        self.client = httpx.Client(headers={"X-API-Key": self.api_key})

    def list_models(self):
        response = self.client.get(self.base_url + "/api/list_models")
        if response.status_code != 200:
            raise ValueError("Error: " + response.text)
        response = response.json()
        return response

    def delete_file(self, filename):
        response = self.client.post(
            self.base_url + "/api/delete_file",
            json={"filename": filename},
        )

        if response.status_code == 404:
            raise FileNotFoundError("Error: " + response.text)
        if response.status_code != 200:
            raise ValueError("Error: " + response.text)
        response = response.json()
        return response

    def list_files(self):
        response = self.client.get(
            self.base_url + "/api/list_files",
        )
        if response.status_code != 200:
            raise ValueError("Error: " + response.text)
        response = response.json()
        return response

    def upload_file(self, path, filename=None):
        if filename is None:
            filename = os.path.basename(path)
        with open(path, "rb") as f:
            response = self.client.post(
                self.base_url + "/api/upload_file",
                files={"file": (filename, f)},
                timeout=60,
            )
        if response.status_code != 200:
            raise ValueError("Error: " + response.text)
        response = response.json()
        return response

    def complete(self, messages, model="auto"):
        data = {"messages": messages, "model": model}
        response = self.client.post(
            self.base_url + "/api/complete",
            json=data,
            timeout=60,
        )
        if response.status_code != 200:
            raise ValueError("Error: " + response.text)
        response = response.json()
        return response


def main():
    debug_url = "http://127.0.0.1:5000"
    debug_api_key = "9cba10db38d29db7b9f03503ef46146c1a431275d05c5c9a2fd278308c0d785d"
    client = Client(debug_url, api_key=debug_api_key)
    print("Models: ", client.list_models())

    test_file = "test.txt"
    with open(test_file, "w") as f:
        f.write("The name of the CEO of Liquid is Ramin Hasani.")
    response = client.upload_file(test_file)
    print(f"Uploaded {test_file} to {response['filename']}")
    files = client.list_files()
    print(f"Files: {files}")

    chat = [
        {"role": "user", "content": "Who is the CEO of Liquid?", "files": ["test.txt"]}
    ]
    response = client.complete(chat)
    print(f"Response: {response['message']['content']}")

    client.delete_file(test_file)
    print(f"Deleted {test_file}")

    files = client.list_files()
    print(f"Files: {files}")

    chat = [{"role": "user", "content": "Hello, world!"}]
    response = client.complete(chat)
    print(f"Response: {response['message']['content']}")


if __name__ == "__main__":
    main()
