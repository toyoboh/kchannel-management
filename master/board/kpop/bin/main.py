import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

url = "https://ja.wikipedia.org/wiki/韓国のアイドルグループ一覧"
res_data = requests.get(url)

# html解析
soup = BeautifulSoup(res_data.text, 'html.parser')

# kpopのグループ名を格納する配列
# これをもとにCSVファイルを作成する
group_list = []

# 連想配列に使用する固定のデータ
CATEGORY_ID  = 3 # kpopのカテゴリーIDを指定する（必要があれば変更する）
ACCOUNT_ID   = 1 # 管理者のID
NOW_DATETIME = datetime.now().strftime('%Y-%m-%d %H:%M:%S') # 連想配列作成時に登録・更新日時に使用するための現在の日付データ

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
            'created_account_id': 1,
            'updated_at'        : NOW_DATETIME,
            'updated_account_id': 1,
            'deleted_at'        : 'NULL',
            'deleted_account_id': 'NULL'
        }

        # 配列に格納
        group_list.append(data)

# CSVファイルの作成
df = pd.DataFrame(group_list)
df.to_csv('../data/information.csv', index = False)

# # kpopグループの名前を抽出し、ファイルに書き込む
# # for構文が1つ増えるため速度は多少遅くなるが、コードの見やすさを優先するためこの書き方とする
# with open("../data/information.txt", "w") as information_file:
#     # グループの要素数と配列の最後のインデックス番号を取得
#     group_list_num = len(group_list)
#     last_index_num = group_list_num - 1 # 配列が最後か判定するために使用

#     for j in range(group_list_num):
#         # 配列の最後のみ改行文字を付け加えない
#         if j == last_index_num:
#             information_file.write(group_list[j])
#         else:
#             information_file.write(group_list[j] + '\n')
