
from datasets import load_dataset
import liquidai
from tqdm import tqdm


def create_qa(row):
    return f"""
            Code: {str(row["func"])}

            Answer:
        """, str(row["target"])


def main():
    # Don't forget to set the LIQUID_URL and LIQUID_API_KEY environment variable
    client = liquidai.Client()
    dataset = load_dataset(
        "code_x_glue_cc_defect_detection")
    preprompt = """
    Given a function, determine whether it is an insecure code that may attack software systems or have any security issues. Answer "True" for insecure code or "False" for secure code. Do not output anything else.
    """
    test_set = dataset["test"]

    num_correct = 0
    num_total = 0
    pbar = tqdm(total=len(test_set))

    for row in test_set:
        q, a = create_qa(row)
        prompt = preprompt + q
        chat = [{"role": "user", "content": prompt}]
        response = client.complete(chat)
        llm_answer = response["message"]["content"]
        llm_answer = str(llm_answer.replace(" ", ""))
        print("llm_answer", llm_answer)
        label_answer = str(a)
        if llm_answer == label_answer:
            num_correct += 1
        num_total += 1
        pbar.update(1)
        pbar.set_description(f"Accuracy: {num_correct*100.0/num_total:0.2f}%")
    pbar.close()


if __name__ == "__main__":
    main()
