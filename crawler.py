import requests
from bs4 import BeautifulSoup

def fetch_wikipedia_description(food_name):
    url = f"https://en.wikipedia.org/wiki/{food_name.replace(' ', '_')}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException:
        return "No description available."

    soup = BeautifulSoup(response.content, 'html.parser')
    description = ""

    # 获取页面第一个段落
    for paragraph in soup.find_all('p'):
        if paragraph.text.strip():
            description = paragraph.text.strip()
            break

    if not description:
        description = "No description available."

    return description
