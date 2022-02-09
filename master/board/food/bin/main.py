import sys
sys.path.append('../../../../')
from common.common import patterns_replace
from bs4           import BeautifulSoup
from datetime      import datetime
import pandas as pd
import requests
import urllib.request

# 抽出対象URL
url = 'https://www.pusannavi.com/special/5047301/index.html'

# 対象URLにアクセスしデータを取得およびhtml解析
res_data = requests.get(url)
res_data.encoding = res_data.apparent_encoding # 文字化け対策
soup = BeautifulSoup(res_data.text, 'html.parser')

# 料理名を格納する配列
# これをもとにCSVファイルを作成する
food_list = []

# 連想配列に使用する固定のデータ
CATEGORY_ID  = 4 # 「韓国料理」のカテゴリーIDを指定する（必要があれば変更する）
ACCOUNT_ID   = 1 # 管理者のID
NOW_DATETIME = datetime.now().strftime('%Y-%m-%d %H:%M:%S') # 連想配列作成時に登録・更新日時に使用するための

# 料理名が入っている全部の要素（タグ）取得
food_elements = soup.find_all(class_='atc_r_ttl')

# 取得された要素から料理名を取得（不要な文字は取り除く）し、料理名配列に格納する
for element in food_elements:
    food_name = element.text
    clean_food_name = patterns_replace(food_name, [' ', '　', '\n'], '')

    # CSVに出力するための配列
    data = {
        'category_id'       : CATEGORY_ID,
        'board_id'          : None,
        'board_name'        : clean_food_name,
        'created_at'        : NOW_DATETIME,
        'created_account_id': ACCOUNT_ID,
        'updated_at'        : NOW_DATETIME,
        'updated_account_id': ACCOUNT_ID,
        'deleted_at'        : 'NULL',
        'deleted_account_id': 'NULL'
    }

    # 配列に追加
    food_list.append(data)

# CSV作成
df = pd.DataFrame(food_list)
df.to_csv('../data/information.csv', index = False)
