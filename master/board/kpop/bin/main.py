from bs4      import BeautifulSoup
from datetime import datetime
import pandas as pd
import requests

url = "https://ja.wikipedia.org/wiki/韓国のアイドルグループ一覧"
res_data = requests.get(url)

# html解析
soup = BeautifulSoup(res_data.text, 'html.parser')

# kpopのグループ情報を管理する配列
# これをもとにCSVファイルを作成する
group_list = []

# 連想配列に使用する固定のデータ
CATEGORY_ID  = 3 # kpopのカテゴリーIDを指定する（必要があれば変更する）
ACCOUNT_ID   = 1 # 管理者のID
NOW_DATETIME = datetime.now().strftime('%Y-%m-%d %H:%M:%S') # 連想配列作成時に登録・更新日時に使用するための

# 年代別にグループがまとめられているので、全テーブルからグループ名を取得し、配列に格納する
for table in soup.find_all(class_='wikitable'):
    # テーブルの全行と行数を取得
    group_detail = table.find_all('tr')
    group_detail_num = len(group_detail)
    
    # テーブルの先頭2行は不要なのでのぞいて処理をする
    for i in range(2, group_detail_num):
        # 行のtdと行に存在するtdの数を取得する
        items = group_detail[i].find_all('td')
        items_num = len(items)

        # tdにてrowspanが指定されている行の場合、2番目のtdにグループ名がある
        if(items_num == 8):
            group_name = items[1].text
        else:
            group_name = items[0].text

        # 改行文字の数がものによって異なるため、一度改行文字を削除する
        clean_group_name = group_name.replace('\n', '')

        # CSVに出力するための配列
        data = {
            'category_id'       : CATEGORY_ID,
            'board_id'          : None,
            'board_name'        : clean_group_name,
            'created_at'        : NOW_DATETIME,
            'created_account_id': ACCOUNT_ID,
            'updated_at'        : NOW_DATETIME,
            'updated_account_id': ACCOUNT_ID,
            'deleted_at'        : 'NULL',
            'deleted_account_id': 'NULL'
        }

        # 配列に格納
        group_list.append(data)

# CSVファイルの作成
df = pd.DataFrame(group_list)
df.to_csv('../data/information.csv', index = False)
