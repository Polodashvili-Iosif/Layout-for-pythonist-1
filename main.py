import argparse
import datetime
from collections import defaultdict
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape

def main():
    parser = argparse.ArgumentParser(
        description='Программа принимает на вход xlsx файл и берёт '
                    'из него информацию о винах. '
                    'В соответствии с информацией из файла '
                    'программа создаёт html файл сайта '
                    'магазина авторского вина "Новое русское вино".'
    )
    parser.add_argument('--file_path_xlsx',
                        help='путь к xlsx файлу с информацией о винах',
                        default='wine.xlsx'
                        )
    wines = pandas.read_excel(parser.parse_args().file_path_xlsx,
                              sheet_name='Лист1',
                              na_values=None,
                              keep_default_na=False).to_dict(orient='records')

    grouped_wines = defaultdict(list)

    for wine in wines:
        grouped_wines[wine['Категория']].append(wine)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )

    template = env.get_template('template.html')

    winery_foundation_year = 1920
    winery_age = datetime.date.today().year - winery_foundation_year

    rendered_page = template.render(
        winery_age=winery_age,
        wines=grouped_wines,
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()

if __name__ == '__main__':
    main()
