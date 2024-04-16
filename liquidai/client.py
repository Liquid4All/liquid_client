import httpx
import os
import json


class Client:
    def __init__(self, base_url=None, api_key=None):
        if base_url is None:
            if "LIQUID_URL" not in os.environ:
                raise ValueError(
                    "URL key not found. Please set LIQUID_URL environment variable or pass in the base_url argument."
                )
            base_url = os.environ["LIQUID_URL"]
        if api_key is None:
            if "LIQUID_API_KEY" not in os.environ:
                raise ValueError(
                    "API key not found. Please set LIQUID_API_KEY environment variable or pass in the api_key argument."
                )
            api_key = os.environ["LIQUID_API_KEY"]
        if base_url.endswith("#"):
            base_url = base_url[:-1]
        if base_url.endswith("/"):
            base_url = base_url[:-1]
        self.base_url = base_url
        self.api_key = api_key
        self.client = httpx.Client(headers={"X-API-Key": self.api_key})

    def _check_for_errors(self, response):
        if response.status_code == 404:
            raise FileNotFoundError("Error: " + response.text)
        elif response.status_code == 403:
            raise PermissionError(
                "Your API Key was not accepted by the server. Make sure you have the correct API Key."
            )
        elif response.status_code == 500:
            raise ValueError(
                "Sever error. Please try again later or contact your administrator."
            )
        elif response.status_code != 200:
            raise ValueError("Error: " + response.text)

    def list_models(self):
        """List all available models.
        returns: A list of model names"""

        response = self.client.get(self.base_url + "/list_models")
        self._check_for_errors(response)
        response = response.json()
        return response

    def delete_file(self, filename):
        """Deletes a file.
        filename: The name of the file to delete."""
        payload = json.dumps({"name": filename})  # Manually prepare the JSON payload

        response = self.client.post(
            self.base_url + "/delete_file",
            json={"name": filename},
        )
        self._check_for_errors(response)
        response = response.json()
        return response

    def list_files(self):
        """List all files stored on the server by the user.
        returns: A list of filenames"""

        response = self.client.get(
            self.base_url + "/list_files",
        )
        self._check_for_errors(response)
        response = response.json()
        return response

    def upload_file(self, path, filename=None):
        """Uploads a file to the server.
        path: The path to the file to upload.
        filename: The name of the file to upload. If None, the basename of path is used.
        """

        if filename is None:
            filename = os.path.basename(path)
        with open(path, "rb") as f:
            print(f)
            response = self.client.post(
                self.base_url + "/upload_file",
                files={"file": (filename, f)},
                timeout=60,
            )
        self._check_for_errors(response)
        response = response.json()
        return response

    def complete(
        self,
        messages,
        model="liquid-beacon-1.0",
        max_new_tokens=384,
        top_p=0.9,
        temperature=0.9,
        top_k=0,
    ):
        """Completes a conversation.
        messages: A list of messages. Each message is a dictionary with the following keys: role, content, files.
        model: The name of the model to use. If None, the default model is used.
        returns: A dictionary containing the response message.
        """

        data = {
            "messages": messages,
            "model": model,
            "max_new_tokens": max_new_tokens,
            "top_p": top_p,
            "temperature": temperature,
            "top_k": top_k,
        }
        response = self.client.post(
            self.base_url + "/complete",
            json=data,
            timeout=60,
        )
        self._check_for_errors(response)
        response = response.json()
        if response["status"] == "error":
            raise ValueError("Error: " + response["message"])
        return response


def main():
    debug_url = "http://127.0.0.1:5000"
    debug_api_key = "2e98dece1646d241908e629fda51d4699e92f6ffc89ac8b4a04c5952ccc8c4cb"
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

    chat = [{"role": "user", "content": "Hello world in python?"}]
    response = client.complete(chat)
    print(f"Response: {response['message']['content']}")
    chat.append(response["message"])
    chat.append({"role": "user", "content": "And in C++?"})
    response = client.complete(chat)
    print(f"Response (default): {response['message']['content']}")
    response = client.complete(chat, temperature=1.5)
    print(f"Response (high T): {response['message']['content']}")
    response = client.complete(chat, max_new_tokens=10)
    print(f"Response (only 10 tokens): {response['message']['content']}")


if __name__ == "__main__":
    main()
