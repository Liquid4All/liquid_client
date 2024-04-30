# labs.liquid.ai API

Openai compatible apis provided by liquid.ai

## Chat Completion
- Input
```
curl --location 'https://labs.liquid.ai/api/v1/chat/completions' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <api-key>' \
--data '{
  "messages": [
    {
      "role": "user",
      "content": "What is the largest animal on earth? Explain the aniaml features in detail. "
    }
  ],
  "model": "liquid-preview-0.1",
  "max_new_tokens": 2048,
  "top_p": 0.9,
  "temperature": 0.9,
  "top_k": 0
}'
```

- Output
```
{
    "id": "cmpl-289eaf41592444718a4a3096d705e5d8",
    "choices": [
        {
            "finish_reason": "stop",
            "index": 0,
            "logprobs": null,
            "message": {
                "content": "The largest animal on Earth is the Blue Whale (Balaenoptera musculus). It is a marine mammal belonging to the baleen whale group, characterized by its massive size, long and slender body, and absence of teeth.",
                "role": "assistant",
                "function_call": null,
                "tool_calls": null
            }
        }
    ],
    "created": 41593,
    "model": "liquid-preview-0.1",
    "object": "chat.completion",
    "system_fingerprint": null,
    "usage": {
        "completion_tokens": 657,
        "prompt_tokens": 29,
        "total_tokens": 686
    }
}
```

## Embedding
- Input
You can adjust dimensions for the embedding output to trade accuracy with speed. The max dimension is 768.
```
curl --location 'https://labs.liquid.ai/api/v1/embeddings' \
--header 'Content-Type: application/json' \
--header 'X-API-Key: <api-key>' \
--data '{
    "input": [
        "My name is ",
        "The president of the United States is ",
        "The future of AI is "
    ],
    "model": "liquid-embedding-0",
    "encoding_format": "float",
    "dimensions": 64
}'
```
- Output
```

{
    "object": "list",
    "data": [
        {
            "object": "embedding",
            "embedding": [
                0.0429396778345108,
                -0.1442646086215973,
                ... total 64 elements
                -0.014958425424993038,
                0.21451351046562195
            ],
            "index": 0
        },
        {
            "object": "embedding",
            "embedding": [
                -0.014381556771695614,
                0.15145191550254822,
                ... total 64 elements
                -0.008231429383158684,
                0.08554109185934067
            ],
            "index": 1
        },
        {
            "object": "embedding",
            "embedding": [
                -0.09036727249622345,
                0.18065275251865387,
                ... total 64 elements
                -0.014518562704324722,
                0.10919401794672012
            ],
            "index": 2
        }
    ],
    "model": "liquid-embedding-0",
    "usage": {
        "prompt_tokens": 21,
        "total_tokens": 21
    }
}
```