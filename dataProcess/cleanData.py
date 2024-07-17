import pandas as pd
import json
import os
import re
from bs4 import BeautifulSoup


folder_path = '/Users/apple/Desktop/2024summer/ECE450J/code'



def clean_text(text):
    text = BeautifulSoup(text, "html.parser").get_text()
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s]', '', text)
    return text


for filename in os.listdir(folder_path):
    if filename.endswith('.json'):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        df = pd.DataFrame(data)

        # 删除重复数据
        df = df.drop_duplicates()

        # 处理缺失值
        df['summary'] = df['summary'].fillna('No summary available')

        # 数据格式化
        df['title'] = df['title'].str.lower()
        df['summary'] = df['summary'].str.lower()

        # 去除无关字符
        df['title'] = df['title'].apply(clean_text)
        df['summary'] = df['summary'].apply(clean_text)

        # 规范化数据
        df['link'] = df['link'].apply(lambda x: 'http://' + x if not x.startswith('http') else x)

        # 转换回列表格式
        cleaned_data = df.to_dict(orient='records')

        cleaned_file_path = os.path.join(folder_path, f'cleaned_{filename}')
        with open(cleaned_file_path, 'w', encoding='utf-8') as cleaned_file:
            json.dump(cleaned_data, cleaned_file, ensure_ascii=False, indent=4)

        print(f"Data cleaning completed and saved to '{cleaned_file_path}'")

