
from datasets import load_dataset
import liquidai
from tqdm import tqdm


def get_prompt(dataset):
    preprompt = """
    You are a binary classfier to check the two functions provided are semantic equivalent or not. Given func1 and func2, answer either "True" or "False". Do not output anything else.
    ==========
    Examples:
    """
    examples = []
    for i, row in enumerate(dataset):
        if len(examples) >= 5:
            break
        examples.append(
            f"""
            Example {i}:
            func1: {str(row["func1"])}
            func2: {str(row["func2"])}
            Answer: {str(row["label"])}
                        """)
    example_prompt = "\n\n".join(examples)
    end_prompt = """
        ==================
        Now start:
    """
    return preprompt + example_prompt + end_prompt


def create_qa(row):
    return f"""
            func1: {str(row["func1"])}
            func2: {str(row["func2"])}
            Answer:
        """, row["label"]


def main():
    # Don't forget to set the LIQUID_URL and LIQUID_API_KEY environment variable
    client = liquidai.Client()
    dataset = load_dataset(
        "code_x_glue_cc_clone_detection_big_clone_bench")
    traning_set = dataset["train"]
    preprompt = get_prompt(traning_set)
    test_set = dataset["test"]

    num_correct = 0
    num_total = 0
    print(len(test_set))
    pbar = tqdm(total=len(test_set))

    for row in test_set:
        q, a = create_qa(row)
        prompt = preprompt + q
        chat = [{"role": "user", "content": prompt}]
        response = client.complete(chat)
        llm_answer = response["message"]["content"]
        llm_answer = str(llm_answer.replace(" ", ""))
        label_answer = str(a)
        print(
            f"llm_answer: {llm_answer} {type(llm_answer)}, label answer: {label_answer} {type(label_answer)}")
        if llm_answer == label_answer:
            num_correct += 1
        num_total += 1
        pbar.update(1)
        pbar.set_description(f"Accuracy: {num_correct*100.0/num_total:0.2f}%")
    pbar.close()


if __name__ == "__main__":
    main()
