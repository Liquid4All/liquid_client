from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from pathlib import Path
import argparse
import liquidai

"""
This example is used to test https://labs.liquid.ai with the API versioning string as api/v1/. Switch branch `git branch api-v1` before proceeding.

Add environment variables
```bash
export LIQUID_URL="https://labs.liquid.ai"
export LIQUID_API_KEY="9cba1....."
```
"""


def get_completion(client, prompt):
    try:
        chat = [{"role": "user", "content": prompt}]
        response = client.complete(chat)
        generated_text = response["message"]["content"]
        print(f"\n\n=========Response: {generated_text}")
        return generated_text
    except Exception as e:
        print(f"Failed to get completion. Error: {e}")
        return None


def send_requests_in_parallel(client, prompt_file):
    file_path = Path(__file__).parent / prompt_file
    prompts = []
    with open(file_path, "r") as file:
        prompts = [line.strip() for line in file.readlines()]

    prompts = [
        f"<|im_start|>system\nYou are Kazu, a helpful assistant by Liquid AI.\n<|im_start|>user\n{p}<|im_end|>\n<|im_start|>assistant\n"
        for p in prompts
    ]
    print("Number of prompts:", len(prompts))
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=len(prompts)) as executor:
        # Submit tasks to the executor
        futures = [executor.submit(get_completion, client, prompt) for prompt in prompts]

        # Wait for the futures to complete and print their results
        num_completed = 0
        num_failed = 0
        for future in as_completed(futures):
            completion = future.result()
            if completion:
                print("\n\n=======Completion result:", completion)
                num_completed += 1
            else:
                print("Failed to get a completion.")
                num_failed += 1

    end_time = time.time()
    total_time = end_time - start_time
    print(
        f"Total time to generate responses: {total_time} seconds. Completed: {num_completed}, Failed: {num_failed}"
    )


if __name__ == "__main__":
    client = liquidai.Client()
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompts", type=str, default="long_prompts.txt")
    args = parser.parse_args()

    send_requests_in_parallel(client=client, prompt_file=args.prompts)
