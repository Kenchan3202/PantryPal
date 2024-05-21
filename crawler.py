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


def fetch_food_storage_info():
    url = "https://food.unl.edu/free-resource/food-storage#fruit"
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    food_storage_info = {}

    # finding
    sections = soup.find_all('div', class_='field-item even')
    for section in sections:
        heading = section.find('h2')
        if heading and "Room temperature" in heading.text:
            items = section.find_all('tr')
            for item in items:
                columns = item.find_all('td')
                if len(columns) >= 2:
                    food_name = columns[0].text.strip()
                    storage_time = columns[1].text.strip()
                    food_storage_info[food_name] = storage_time

    return food_storage_info


food_storage_info = fetch_food_storage_info()
print(food_storage_info)