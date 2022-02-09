from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import requests

# URL情報
end_words = ['あ', 'か', 'さ', 'た', 'な・わ', 'は', 'ま', 'や・ら']
base_url  = 'https://ja.wikipedia.org/wiki/韓国のテレビドラマ一覧_'

# ドラマ情報格納配列（CSVファイル作成に使う）
drama_list = []

# CSVファイル出力のための配列作成
for end_word in end_words:
    
    # 使用するURLの定義
    url = base_url + end_word

    # リクエストおよびHTML解析
    res_data = requests.get(url)
    soup     = BeautifulSoup(res_data.text, 'html.parser')

    # 連想配列に使用する固定のデータ
    CATEGORY_ID  = 4 # ドラマのカテゴリーIDを指定する（必要があれば変更する）
    ACCOUNT_ID   = 1 # 管理者のID
    NOW_DATETIME = datetime.now().strftime('%Y-%m-%d %H:%M:%S') # 連想配列作成時に登録・更新日時に使用するための

    for table in soup.find_all(class_='wikitable'):
        # テーブルの全行を取得
        detail_rows     = table.find_all('tr')
        detail_rows_num = len(detail_rows)

        for i in range(1, detail_rows_num):

            # 行の先頭のtdにドラマの日本語名が入っている
            drama_name       = detail_rows[i].td.text

            # 改行コードが存在する可能性があるので取り除く
            clean_drama_name = drama_name.replace('\n', '')

            # CSVに出力するための配列
            data = {
                'category_id'       : CATEGORY_ID,
                'board_id'          : None,
                'board_name'        : clean_drama_name,
                'created_at'        : NOW_DATETIME,
                'created_account_id': ACCOUNT_ID,
                'updated_at'        : NOW_DATETIME,
                'updated_account_id': ACCOUNT_ID,
                'deleted_at'        : 'NULL',
                'deleted_account_id': 'NULL'
            }

            # 配列に格納
            drama_list.append(data)

# CSVファイルの作成
df = pd.DataFrame(drama_list)
df.to_csv('../data/information.csv', index = False)
