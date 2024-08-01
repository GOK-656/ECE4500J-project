from collections import deque
from process import load_examples
from process import extract_json_content
from openai import OpenAI
from pathlib import Path
import xml.etree.ElementTree as ET
import json
import time

class Client:
    def __init__(self):
        KIMI_API_KEY = 'sk-rxptwe2HlYmsCJftVB4kILBUUd7bLM4bZdGny3NP1e2sXrh2'
        DEEPSEEK_API_KEY = 'sk-697c7886451f48ec92f35bdefc368e5e'
        self.kimi_client = OpenAI(
            api_key=f"{KIMI_API_KEY}",
            base_url="https://api.moonshot.cn/v1",
        ) # For OCR
        # self.deepseek_client = OpenAI(
        #     api_key=f"{DEEPSEEK_API_KEY}",
        #     base_url="https://api.deepseek.com/v1",
        # ) # For Chat
        self.deepseek_client = self.kimi_client

        self.examples = load_examples()
        self.setting = [
            {"role": "system", "content": "You are a professional business consultant. You are helping a client to "
                                          "build a business model canvas (BMC). You should return as json format for "
                                          "each of the keys: key_partners, key_activities, key_resources, "
                                          "value_propositions, customer_relationships, channels, customer_segments, "
                                          "cost_structure, revenue_streams according to the information provided. "
                                          "Each key should be a list of strings. The client will provide you with the "
                                          "information needed to generate the BMC. You should generate the BMC based "
                                          "on the information provided by the client. If the client asks you to modify "
                                          "a specific key, you should modify that key and keep everything else "
                                          "unchanged. "},
            {"role": "system", "content": "Here are some good BMC examples: " + self.examples[0] + self.examples[1]}
        ]
        self.history = deque([], maxlen=5)

    def chat(self, prompt):
        self.history.append({
            "role": "user",
            "content": prompt
        })
        ans = ''
        while len(ans.strip()) == 0:
            input_message = self.setting + list(self.history)
            completion = self.deepseek_client.chat.completions.create(
                # model="deepseek-chat",
                model="moonshot-v1-8k",

                messages=input_message,

                response_format={"type": "json_object"},

                n=1,
            )
            ans = completion.choices[0].message.content
            print(f"Answer: {ans}")
            if len(ans.strip()) > 0:
                self.history.append({
                    "role": "assistant",
                    "content": ans
                })
                break
            time.sleep(1)
        return ans

    def file2text(self, file_path):
        '''将文件转化为xml格式的txt, 根据anthropic文档使用xml格式更有效'''

        # 调用kimi的api
        file_object = self.kimi_client.files.create(file=Path(file_path), purpose="file-extract")
        file_content = self.kimi_client.files.content(file_id=file_object.id).text
        content = json.loads(file_content)

        # 创建xml字符串
        root = ET.Element("files")
        file_element = ET.SubElement(root, "file")
        for key, value in content.items():
            child = ET.SubElement(file_element, key)
            child.text = value
        xml_str = ET.tostring(root, encoding='unicode')
        print("XML file str: \n" + xml_str + "\n")
        return xml_str

    def files2text(self, folder_path):
        '''将文件夹内所有文件转化为xml格式的txt, 根据anthropic文档使用xml格式更有效'''
        root = ET.Element("files")
        # 调用kimi的api
        for file_path in Path(folder_path).glob('*'):
            file_object = self.kimi_client.files.create(file=file_path, purpose="file-extract")
            file_content = self.kimi_client.files.content(file_id=file_object.id).text
            content = json.loads(file_content)
            file_element = ET.SubElement(root, "file")
            for key, value in content.items():
                child = ET.SubElement(file_element, key)
                child.text = value
        xml_str = ET.tostring(root, encoding='unicode')
        print("XML files str: \n" + xml_str + "\n")
        return xml_str

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