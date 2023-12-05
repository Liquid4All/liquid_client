from datasets import load_dataset
import liquidai
from tqdm import tqdm


def make_question(sample):
    """Convert a sample from the ARC dataset into a question prompt and answer."""

    text = "Question: " + sample["question"]
    for i in range(len(sample["choices"]["text"])):
        text += f"\n{sample['choices']['label'][i]}) {sample['choices']['text'][i]}"
    text += "\nAnswer:"
    return text, sample["answerKey"]


def main():
    debug_url = "http://127.0.0.1:5000"
    debug_api_key = "9cba10db38d29db7b9f03503ef46146c1a431275d05c5c9a2fd278308c0d785d"

    client = liquidai.Client(debug_url, api_key=debug_api_key)
    print("Models: ", client.list_models())

    test_ds = load_dataset("ai2_arc", "ARC-Challenge")["test"]
    preprompt = "Answer the following multiple choice question. Output the letter corresponding to the correct answer.\n"

    num_correct, num_total = 0, 0
    pbar = tqdm(total=len(test_ds))
    for i, sample in enumerate(test_ds):
        q, a = make_question(sample)
        prompt = preprompt + q

        chat = [{"role": "user", "content": prompt}]
        response = client.complete(chat)
        llm_answer = response["message"]["content"]
        llm_answer = llm_answer.strip(" \n")
        if len(llm_answer) > 0 and llm_answer[0] == a[0]:
            num_correct += 1
        num_total += 1
        pbar.update(1)
        pbar.set_description(f"Accuracy: {num_correct*100.0/num_total:0.2f}%")
    pbar.close()


if __name__ == "__main__":
    main()
