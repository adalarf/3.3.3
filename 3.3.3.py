import requests
import json
import pandas as pd


def get_page(i, j, page = 0):
    params = {
        'specialization': 1,
        'date_from': f'2022-12-16T{i}:00:01+0300',
        'date_to': f'2022-12-16T{j}:59:59+0300',
        'page': page,
        'per_page': 100
    }

    req = requests.get('https://api.hh.ru/vacancies', params)
    data = req.content.decode()
    req.close()
    return data

js_objs = []

def get_hours(i, j):
    for page in range(0, 20):
        js_obj = json.loads(get_page(i, j, page))
        js_objs.extend(js_obj["items"])

        if (js_obj['pages'] - page) <= 1:
            break

get_hours('00', '03')
get_hours('04','06')
get_hours('07','09')
get_hours('10','12')
get_hours('13', '15')
get_hours('16', '18')
get_hours('19', '21')
get_hours('22','23')


def extract_from_dict(value1, value2):
    result = []
    for i in range(0, len(value1)):
        if value1[i] == None:
            result.append(value1[i])
        else:
            result.append(value1[i][value2])
    return result

name = []
salary_from = []
salary_to = []
salary_currency = []
area_name = []
published_at = []
for i in range(0, len(js_objs)):
    name.append(js_objs[i]['name'])
    salary_from.append(js_objs[i]['salary'])
    salary_to.append(js_objs[i]['salary'])
    salary_currency.append(js_objs[i]['salary'])
    area_name.append(js_objs[i]['area'])
    published_at.append(js_objs[i]['published_at'])

dict_params = {
    'name': name,
    'salary_from': extract_from_dict(salary_from, 'from'),
    'salary_to': extract_from_dict(salary_to, 'to'),
    'salary_currency': extract_from_dict(salary_currency, 'currency'),
    'area_name': extract_from_dict(area_name, 'name'),
    'published_at': published_at
}

dict_df = pd.DataFrame(dict_params)
dict_df.to_csv('data.csv', index=False)