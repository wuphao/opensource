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

# import pygal
# from pygal.style import LightColorizedStyle as LCS, LightenStyle as LS
# names, plot_dicts = [], []
# for repo_dict in result:
#     value = int(repo_dict[1][0])*1000+int(repo_dict[1][2])*100
#     names.append(repo_dict[0])
#     description = repo_dict[3]
#     if not description:
#         description = "No description provided."
#
#     plot_dict = {
#         'value': value,
#         'label': description,
#         'xlink': repo_dict[2],
#         }
#     plot_dicts.append(plot_dict)
# my_style = LS('#333366', base_style=LCS)
# my_style.title_font_size = 24
# my_style.label_font_size = 14
# my_style.major_label_font_size = 18
#
# my_config = pygal.Config()
# my_config.x_label_rotation = 45
# my_config.show_legend = False
# my_config.truncate_label = 15
# my_config.show_y_guides = False
# my_config.width = 1000
#
# chart = pygal.Bar(my_config, style=my_style)
# chart.title = 'Most-Starred Python Projects on Gitee'
# chart.x_labels = names
#
# chart.add('', plot_dicts)
# chart.render_to_file('python_repos.svg')

