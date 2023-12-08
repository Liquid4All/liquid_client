import liquidai


if __name__ == "__main__":
    # Don't forget to set the LIQUID_URL and LIQUID_API_KEY environment variable
    client = liquidai.Client()
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
    print(f"Response: {response['message']['content']}")
