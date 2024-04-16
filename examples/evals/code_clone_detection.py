from datasets import load_dataset
import liquidai
from tqdm import tqdm
import re


def create_qa(row):
    return (
        f"""
            func1: {str(row["func1"])}
            func2: {str(row["func2"])}
            Answer:
        """,
        row["label"],
    )


def clean_string(s):
    # Remove all whitespace and convert to lower case for case insensitive comparison
    return re.sub(r"\s+", "", s).lower()


def main():
    # Don't forget to set the LIQUID_URL and LIQUID_API_KEY environment variable
    client = liquidai.Client()
    dataset = load_dataset("code_x_glue_cc_clone_detection_big_clone_bench")
    test_set = dataset["test"]
    preprompt = """
    Given the code of two functions 'func2' and 'func2', determine whether they implement the same function or not. Answer either "True" or "False". Do not output anything else.
    """
    num_correct = 0
    num_total = 0
    print(len(test_set))
    pbar = tqdm(total=len(test_set))

    for row in test_set:
        q, a = create_qa(row)
        prompt = preprompt + q
        chat = [{"role": "user", "content": prompt}]
        response = client.complete(chat)
        llm_answer = clean_string(response["message"]["content"])
        label_answer = clean_string(str(a))
        if llm_answer == label_answer:
            num_correct += 1
        num_total += 1
        pbar.update(1)
        pbar.set_description(f"Accuracy: {num_correct*100.0/num_total:0.2f}%")
    pbar.close()


if __name__ == "__main__":
    main()
