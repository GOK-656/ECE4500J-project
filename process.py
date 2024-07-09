import json

def chat(client, message):
    completion = client.chat.completions.create(
        # 👇 这里指定 Kimi 的模型名称
        model="moonshot-v1-8k",

        messages=[
            {"role": "user",
             "content": message + ' According to the information above, construct a Business Canvas Model. '
                                  'Return as json format for each of the keys: key_partners, key_activities, '
                                  'key_resources, value_proposition, customer_relationship, channels, customer_segments'
                                  ', cost_structure, revenue_streams.'}
        ],

        response_format={"type": "json_object"},
        n=1

    )
    return completion.choices[0].message.content

def parse_answer(answer):
    # TODO: parse the response by keys of the BMC
    parsed_ans = json.loads(answer)
    new_ans = {}
    for k, v in parsed_ans.items():
        if type(v) is not list:
            new_ans[k] = [v]
        else:
            new_ans[k] = v
    return new_ans
    # return {
    #     "key_partners": "this is some random answer",
    #     "key_activities": "this is some random answer"*5,
    #     "key_resources": "this is some random answer",
    #     "value_proposition": "this is some random answer",
    #     "customer_relationship": "this is some random answer",
    #     "channels": "this is some random answer"*10,
    #     "customer_segments": "this is some random answer",
    #     "cost_structure": "this is some random answer",
    #     "revenue_streams": "this is some random answer",
    #         }