from openai import OpenAI
from collections import deque


class Client:
    def __init__(self):
        with open('kimi-api.txt', 'r') as f:
            KIMI_API_KEY = f.read().strip()
        self.client = OpenAI(
            api_key=f"{KIMI_API_KEY}",
            base_url="https://api.moonshot.cn/v1",
        )
        self.setting = [
            {"role": "system", "content": "You are a professional business consultant. You are helping a client to "
                                          "build a business model canvas (BMC). You should return as json format for "
                                          "each of the keys: key_partners, key_activities, key_resources, "
                                          "value_proposition, customer_relationship, channels, customer_segments, "
                                          "cost_structure, revenue_streams according to the information provided. "
                                          "Each key should be a list of strings. The client will provide you with the "
                                          "information needed to generate the BMC. You should generate the BMC based "
                                          "on the information provided by the client. If the client asks you to modify "
                                          "a specific key, you should modify that key and keep everything else "
                                          "unchanged. "}
        ]
        self.history = deque([], maxlen=5)

    def chat(self, message):
        self.history.append({
            "role": "user",
            "content": message
        })

        completion = self.client.chat.completions.create(
            # 👇 这里指定 Kimi 的模型名称
            model="moonshot-v1-8k",

            messages=self.setting + list(self.history),

            response_format={"type": "json_object"},
            n=1

        )
        ans = completion.choices[0].message.content
        self.history.append({
            "role": "assistant",
            "content": ans
        })
        return ans

if __name__ == '__main__':
    import time
    client = Client()
    message = 'Generate a random Business Model Canvas.'
    response = client.chat(message)
    print(response)
    print(client.history)
    time.sleep(3)
    message = 'Modify key_partners for a startup company selling drinks. Keep everything else unchanged.'
    response = client.chat(message)
    print(response)
    print(client.history)
