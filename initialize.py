def initialize_api():
    from openai import OpenAI

    with open('kimi-api.txt', 'r') as f:
        KIMI_API_KEY = f.read().strip()

    client = OpenAI(
        api_key=f"{KIMI_API_KEY}",
        base_url="https://api.moonshot.cn/v1",
    )
    return client