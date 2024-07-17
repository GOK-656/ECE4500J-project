from collections import deque
import anthropic
from process import load_examples
from process import extract_json_content

class Client:
    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key="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"
        )
        self.examples = load_examples()
        self.history = deque([], maxlen=5)

    def chat(self, prompt):
        if len(self.history) == 0:
            _messages =[
                        {"role": "system", "content": "You are a professional business consultant. You are helping a client to build a business model canvas (BMC).",
                        
                        "role": "user", "content": prompt + "Here are some examples of industry and BMC:" + self.examples[0] + self.examples[1] + "\n Note: You should ONLY return a JSON dictionary for "
                        "each of the keys: key_partners, key_activities, key_resources, "
                        "value_propositions, customer_relationships, channels, customer_segments, "
                        "cost_structure, revenue_streams according to the information provided. "
                        "Each key should be a list of strings. The client will provide you with the "
                        "information needed to generate the BMC. You should generate the BMC based "
                        "on the information provided by the client. If the client asks you to modify "
                        "a specific key, you should modify that key and keep everything else "
                        "unchanged. "}
                    ]
        else:
            _messages = [
                        {"role": "system", "content": "You are a professional business consultant. You are helping a client to build a business model canvas (BMC).",
                        
                        "role": "user", "content": prompt + "Chat history: " + str(list(self.history))
                        + "\n Note: You should ONLY return a JSON dictionary for "
                        "each of the keys: key_partners, key_activities, key_resources, "
                        "value_propositions, customer_relationships, channels, customer_segments, "
                        "cost_structure, revenue_streams according to the information provided. "
                        "Each key should be a list of strings. The client will provide you with the "
                        "information needed to generate the BMC. You should generate the BMC based "
                        "on the information provided by the client. If the client asks you to modify "
                        "a specific key, you should modify that key and keep everything else "
                        "unchanged. "}
                    ]

        print(_messages)
        message = self.client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=2048,
            messages=_messages
        )
        self.history.append({
            "role": "user",
            "content": message
        })
        output = "\n\n".join(block.text for block in message.content)
        output = extract_json_content(output)
        print(output)
        self.history.append({
            "role": "bot",
            "content": output
        })
        print(self.history)
        return output