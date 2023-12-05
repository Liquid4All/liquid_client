import os
import liquidai


def create_demo_file(path, content):
    with open(path, "w") as f:
        f.write(content)


def main():
    # Don't forget to set the LIQUID_URL and LIQUID_API_KEY environment variable
    client = liquidai.Client()

    path = "demo_folder"
    os.makedirs(path, exist_ok=True)
    # Let's create some demo files in the folder
    # We will create 3 files:
    create_demo_file(os.path.join(path, "file1.txt"), "C. elegans is a nematode.")
    create_demo_file(
        os.path.join(path, "file2.txt"), "C. elegans' nervous system has 302 neurons."
    )
    create_demo_file(os.path.join(path, "file3.txt"), "C. elegans has 959 cells.")

    all_files = os.listdir(path)
    for filename in all_files:
        filepath = os.path.join(path, filename)
        response = client.upload_file(filepath)
        print(f"Uploaded {filepath} to {response['filename']}")

    files = client.list_files()
    print(f"Files: {files}")

    chat = [
        {
            "role": "user",
            "content": "How many neurons does C. elegans have?",
            "files": all_files,
        }
    ]
    response = client.complete(chat)
    print(f"Response: {response['message']['content']}")


if __name__ == "__main__":
    main()
