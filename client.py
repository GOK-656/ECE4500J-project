from openai import OpenAI


class Client:
    def __init__(self):
        with open('kimi-api.txt', 'r') as f:
            KIMI_API_KEY = f.read().strip()
        self.client = OpenAI(
            api_key=f"{KIMI_API_KEY}",
            base_url="https://api.moonshot.cn/v1",
        )

    def chat(self, message):
        completion = self.client.chat.completions.create(
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
