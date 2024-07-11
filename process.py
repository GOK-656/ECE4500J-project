import json


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