# labs.liquid.ai API
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
  "model": "liquid-beacon-1.0",
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
                "content": "The largest animal on Earth is the Blue Whale (Balaenoptera musculus). It is a marine mammal belonging to the baleen whale group, characterized by its massive size, long and slender body, and absence of teeth. Here are some of the notable features of the Blue Whale:\n\n1. Size: Blue whales can grow up to 100 feet (30 meters) in length and can weigh as much as 200 tons (180 metric tonnes). This makes them the largest animals to have ever existed on Earth, larger than even the largest dinosaurs.\n\n2. Body: The body of a blue whale is streamlined, allowing it to move through the water with minimal resistance. They have a small dorsal fin, and their flippers are relatively small compared to other whale species.\n\n3. Color: The upper part of the blue whale's body is a dark blue-gray color, while the underside is a lighter gray. This coloration provides camouflage, helping the whale blend in with the dark depths of the ocean when viewed from above and the lighter surface when viewed from below.\n\n4. Breath: Blue whales can hold their breath for extended periods, up to 90 minutes, and can dive to depths of over 1,000 feet (300 meters). They do this to find food, as they feed on krill, tiny shrimp-like animals, which are found at great depths in the ocean.\n\n5. Feeding: Blue whales are filter feeders, using baleen plates (composed of keratin) in their mouths to filter out krill from the water. They take in a large mouthful of water and krill, and then use their powerful throat muscles to force the water back out through the baleen plates, trapping the krill for consumption.\n\n6. Reproduction: Blue whales reproduce slowly, with females giving birth to a single calf every 2-3 years. The gestation period is approximately 11-12 months, and the calves are nursed for about 6-12 months.\n\n7. Communication: Blue whales communicate using a variety of vocalizations, including moans, groans, and songs. These sounds can be heard from miles away and are used for various purposes, such as finding mates, coordinating group movements, and defending territory.\n\n8. Migration: Blue whales are known for their long-distance migrations, traveling thousands of miles between their feeding and breeding grounds. They migrate to polar waters during the summer months to feed on krill and then move to warmer waters near the equator during the winter to breed and give birth.\n\nIn summary, the Blue Whale is the largest animal on Earth, characterized by its massive size, long and slender body, and unique filter-feeding mechanism. It is a slow-reproducing, long-distance migrator that plays a vital role in the marine ecosystem.",
                "role": "assistant",
                "function_call": null,
                "tool_calls": null
            }
        }
    ],
    "created": 41593,
    "model": "liquid-beacon-1.0",
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