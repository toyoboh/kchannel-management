import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd

# 対象URL
url = 'https://seoul-holic.com/?mode=f8'

# リクエストおよびHTML解析
res_data = requests.get(url)
soup     = BeautifulSoup(res_data.text, 'html.parser')

# 対象のテーブルを取得（先頭のテーブルが対象）
cosme_table = soup.find(id='koreacosme-etc-explanation')

# ループ処理前の設定
cosme_rows     = cosme_table.find_all('tr') # テーブルの全ての行を取得
cosme_rows_num = len(cosme_rows)            # テーブルの行数を取得
loop_num       = cosme_rows_num - 3         # 行末3行は取得対象外なのでその数を引く

# CSVに出力するための定数定義
CATEGORY_ID  = 5 # 対象のカテゴリーID
ACCOUNT_ID   = 1 # 管理者ID
NOW_DATETIME = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# CSV出力に必要な配列
cosme_list = []

for i in range(loop_num):
    # コスメブランド名を取得し、整形する
    cosme_name       = cosme_rows[i].a.text
    clean_cosme_name = cosme_name.replace('\n', '')

    data = {
        'category_id'       : CATEGORY_ID,
        'board_id'          : None,
        'board_name'        : clean_cosme_name,
        'created_at'        : NOW_DATETIME,
        'created_account_id': ACCOUNT_ID,
        'updated_at'        : NOW_DATETIME,
        'updated_account_id': ACCOUNT_ID,
        'deleted_at'        : 'NULL',
        'deleted_account_id': 'NULL'
    }

    cosme_list.append(data)

df = pd.DataFrame(cosme_list)
df.to_csv('../data/information.csv', index = False)
