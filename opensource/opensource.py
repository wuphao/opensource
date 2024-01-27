import requests
from bs4 import BeautifulSoup
import  pandas as pd
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
}
result = []

for num in range(1, 4, 1):
    response = requests.get(f"https://search.gitee.com/?skin=rec&type=repository&q=python&sort=stars_count&lang=python&pageno={num}", headers=headers)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    for item in soup.find_all('div', class_='item'):
        name_element = item.find('a', class_='ns')
        project_name = name_element.text.strip() if name_element else None
        stars_element = item.find('a', class_='tag stars theme-hover')
        stars_count = stars_element.find('em').text.strip() if stars_element else None
        address_element = item.find('a', class_='ns')['href'] if name_element else None
        desc_element = item.find('div', class_='desc')
        project_description = desc_element.text.strip() if desc_element else None
        if project_name and stars_count and address_element and project_description:
            result.append((project_name, stars_count, address_element, project_description))

print(result)
df = pd.DataFrame(result, columns=['name', 'start', 'address', 'description'])

df.to_excel('data.xlsx', index=False)

