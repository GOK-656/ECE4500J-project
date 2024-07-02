from flask import Flask
from flask import render_template, request, url_for
from openai import OpenAI

app = Flask(__name__)

with open('kimi-api.txt', 'r') as f:
    KIMI_API_KEY = f.read().strip()

client = OpenAI(
    # 👇 这里指定 Kimi 的 API Key
    api_key=f"{KIMI_API_KEY}",

    # 👇 这里指定 Kimi 的 API 地址
    base_url="https://api.moonshot.cn/v1",
)

@app.route('/')
def start():  # put application's code here
    return render_template('index.html')

@app.route('/generate', methods=['GET', 'POST'])
def generate():
    if request.method == 'POST':
        message = request.form['idea']
        completion = client.chat.completions.create(
            # 👇 这里指定 Kimi 的模型名称
            model="moonshot-v1-8k",

            messages=[
                {"role": "user",
                 "content": message}
            ],
        )

        return render_template('multimodel.html', content=completion.choices[0].message.content)
    return render_template('multimodel.html')

if __name__ == '__main__':
    app.run()
