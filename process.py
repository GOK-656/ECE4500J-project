import os
import json


def parse_answer(answer):
    # TODO: parse the response by keys of the BMC
    parsed_ans = json.loads(extract_json_content(answer))
    if "bmc" in parsed_ans:
        parsed_ans = parsed_ans["bmc"]
    new_ans = {}

    prefix_dict = {
        "key_partner": "key_partners",
        "key_activit": "key_activities",
        "key_resource": "key_resources",
        "value_proposition": "value_propositions",
        "customer_relationship": "customer_relationships",
        "channel": "channels",
        "customer_segment": "customer_segments",
        "cost_structure": "cost_structure",
        "revenue_stream": "revenue_streams"
    }
    for k, v in parsed_ans.items():
        for prefix, new_key in prefix_dict.items():
            if k.startswith(prefix):
                k = new_key
                break
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

def load_examples():
    # Define the directory containing the JSON files
    directory = 'dataProcess/data'

    # Initialize an empty list to hold the JSON strings
    json_strings = []

    # Iterate over all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                # Read the file content and append to the list
                json_strings.append(file.read())

    # Now json_strings contains all the JSON file contents as strings
    # for i, json_str in enumerate(json_strings):
    #     print(f"Content of file {i+1}: {json_str[:100]}...")  # Print first 100 characters of each file for verification
    return json_strings

def extract_json_content(string):
    start = string.find('{')
    end = string.rfind('}')
    if start == -1 or end == -1:
        raise ValueError("No valid JSON object found in the string")
    return string[start:end+1]