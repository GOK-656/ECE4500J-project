def chat(client, message):
    completion = client.chat.completions.create(
        # 👇 这里指定 Kimi 的模型名称
        model="moonshot-v1-8k",

        messages=[
            {"role": "user",
             "content": message}
        ],
    )
    return completion.choices[0].message.content

def parse_answer(answer):
    # TODO: parse the response by keys of the BMC
    return {
        "key_partners": "this is some random answer",
        "key_activities": "this is some random answer"*5,
        "key_resources": "this is some random answer",
        "value_proposition": "this is some random answer",
        "customer_relationship": "this is some random answer",
        "channels": "this is some random answer"*10,
        "customer_segments": "this is some random answer",
        "cost_structure": "this is some random answer",
        "revenue_streams": "this is some random answer",
            }