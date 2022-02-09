import pandas as pd
import requests
from bs4      import BeautifulSoup
from datetime import datetime


url = 'https://www.arukikata.co.jp/country/KR/info/cities.html'

res_data          = requests.get(url)
res_data.encoding = res_data.apparent_encoding # 文字化け対策
soup              = BeautifulSoup(res_data.text, 'html.parser')

# CSVに出力するための定数定義
CATEGORY_ID  = 5 # 対象のカテゴリーID
ACCOUNT_ID   = 1 # 管理者ID
NOW_DATETIME = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# CSV出力に必要な配列
city_list = []

for list in soup.find_all(class_='list-city'):
    
    for item in list.find_all('li'):

        city_name = item.text
        clean_city_name = city_name.replace('\n', '')

        data = {
            'category_id'       : CATEGORY_ID,
            'board_id'          : None,
            'board_name'        : clean_city_name,
            'created_at'        : NOW_DATETIME,
            'created_account_id': ACCOUNT_ID,
            'updated_at'        : NOW_DATETIME,
            'updated_account_id': ACCOUNT_ID,
            'deleted_at'        : 'NULL',
            'deleted_account_id': 'NULL'
        }

        city_list.append(data)

df = pd.DataFrame(city_list)
df.to_csv('../data/information.csv', index = False)
