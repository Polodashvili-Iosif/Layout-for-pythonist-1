from http.server import HTTPServer, SimpleHTTPRequestHandler
import datetime

from jinja2 import Environment, FileSystemLoader, select_autoescape
from collections import defaultdict
import pandas

wines_info_dic = pandas.read_excel('wine.xlsx',
                                   sheet_name='Лист1',
                                   na_values=None,
                                   keep_default_na=False).to_dict(orient='records')

wines_info = defaultdict(list)

for i in range(len(wines_info_dic)):
    wines_info[wines_info_dic[i]['Категория']].append(wines_info_dic[i])

categories = sorted(dict(wines_info))

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html'])
)

template = env.get_template('template.html')

winery_foundation_date = datetime.date(1920, 1, 1)
winery_age_var = int((datetime.date.today() - winery_foundation_date)
                     / datetime.timedelta(days=365)
                     )

rendered_page = template.render(
    winery_age=winery_age_var,
    wines_info=wines_info,
    categories=categories
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
