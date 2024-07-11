import requests
import json

api_urls = {
    'hardware_manufacturing': [
        'https://www.eetimes.com/wp-json/wp/v2/posts',
        'https://semiengineering.com/wp-json/wp/v2/posts',
        'https://moschip.com/wp-json/wp/v2/posts',
    ],
    'software_development': [
        'https://sdtimes.com/wp-json/wp/v2/posts',
        'https://techcrunch.com/wp-json/wp/v2/posts',
    ],
    'Pharmaceuticals': [
        'https://pharmatimes.com/wp-json/wp/v2/posts',
    ]
}

def fetch_posts(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        posts = response.json()
        posts_data = []
        for post in posts:
            title = post.get('title', {}).get('rendered', 'No title')
            link = post.get('link', 'No link')
            summary = post.get('excerpt', {}).get('rendered', 'No summary')
            posts_data.append({
                'title': title,
                'link': link,
                'summary': summary
            })
        return posts_data
    else:
        print(f"Failed to retrieve posts from {api_url}. Status code: {response.status_code}")
        return []

def main():
    for category, urls in api_urls.items():
        all_posts = []
        for api_url in urls:
            posts_data = fetch_posts(api_url)
            all_posts.extend(posts_data)
        
        with open(f'{category}.json', 'w', encoding='utf-8') as file:
            json.dump(all_posts, file, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    main()
