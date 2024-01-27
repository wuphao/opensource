import pygal
from pygal.style import LightColorizedStyle as LCS, LightenStyle as LS
import pandas as pd

# 从Excel文件加载数据
df = pd.read_excel(r'C:\Users\shangs\Desktop\data.xlsx')

# 为条形图准备数据
names = df['name'].tolist()

# 使用正则表达式移除非数字和小数点，然后将列转换为浮点数，最后转换为整数
stars = df['stars'].astype(str).replace('[^\d.]', '', regex=True).astype(float).astype(int).tolist()

descriptions = df['description'].tolist()

# 为plot_dicts创建字典列表
plot_dicts = []
for name, star, description in zip(names, stars, descriptions):
    plot_dict = {
        'value': star,
        'label': description,
        'xlink': f'https://gitee.com/{name}',
    }
    plot_dicts.append(plot_dict)

# 使用PyGal创建可视化图表
my_style = LS('#333366', base_style=LCS)
my_style.title_font_size = 24
my_style.label_font_size = 14
my_style.major_label_font_size = 18

my_config = pygal.Config()
my_config.x_label_rotation = 45
my_config.show_legend = False
my_config.truncate_label = 15
my_config.show_y_guides = False
my_config.width = 1000

chart = pygal.Bar(my_config, style=my_style)
chart.title = 'Gitee上star最多的Python项目'
chart.x_labels = names

chart.add('', plot_dicts)
chart.render_to_file('gitee_python_repos.svg')