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
        model: str | None = None,
        max_tokens: int | None = None,
        top_p: float | None = None,
        temperature: float | None = None,
    ):
        """Completes a conversation.

        messages: A list of messages. Each message is a dictionary with the following keys: role, content, files.

        model: The name of the model to use. If None, the default model is used.
        returns: A dictionary containing the response message.

        max_tokens: The maximum number of [tokens](/tokenizer) that can be generated in the chat

        temperature: What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.

            We generally recommend altering this or `top_p` but not both.

        top_p: An alternative to sampling with temperature, called nucleus sampling, where the
            model considers the results of the tokens with top_p probability mass. So 0.1
            means only the tokens comprising the top 10% probability mass are considered.

            We generally recommend altering this or `temperature` but not both.

        """

        request_data = {
            "messages": messages,
        }
        if model:
            request_data["model"] = model
        if max_tokens:
            request_data["max_tokens"] = max_tokens
        if top_p:
            request_data["top_p"] = top_p
        if temperature:
            request_data["temperature"] = temperature

        response = self.client.post(
            self.base_url + "/complete",
            json=request_data,
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

    messages = [{"role": "user", "content": "Who is the CEO of Liquid?", "files": ["test.txt"]}]
    response = client.complete(messages)
    print(f"Response: {response['message']['content']}")

    client.delete_file(test_file)
    print(f"Deleted {test_file}")

    files = client.list_files()
    print(f"Files: {files}")

    messages = [{"role": "user", "content": "Hello world in python?"}]
    response = client.complete(messages)
    print(f"Response: {response['message']['content']}")
    messages.append(response["message"])
    messages.append({"role": "user", "content": "And in C++?"})
    response = client.complete(messages)
    print(f"Response (default): {response['message']['content']}")
    response = client.complete(messages, temperature=1.5)
    print(f"Response (high T): {response['message']['content']}")
    response = client.complete(messages, max_tokens=10)
    print(f"Response (only 10 tokens): {response['message']['content']}")


if __name__ == "__main__":
    main()
