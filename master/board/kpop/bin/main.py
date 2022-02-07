import requests
from bs4 import BeautifulSoup

url = "https://ja.wikipedia.org/wiki/韓国のアイドルグループ一覧"
res_data = requests.get(url)

# html解析
soup = BeautifulSoup(res_data.text, 'html.parser')

# kpopグループの名前を抽出し、ファイルに書き込む
with open("../data/information.txt", "w") as information_file:

    # 年代別にグループがまとめられているので、全テーブルを取得して処理をする
    for table in soup.find_all(class_='wikitable'):
        # テーブルの全行と行数を取得
        group_detail = table.find_all('tr')
        group_detail_num = len(group_detail)
        
        # テーブルの先頭2行は不要なのでのぞいて処理をする
        for i in range(2, group_detail_num):
            # 行のtdと行に存在するtdの数を取得する
            items = group_detail[i].find_all('td')
            items_count = len(items)

            # tdにてrowspanが指定されている行の場合、2番目のtdにグループ名がある
            if(items_count == 8):
                group_name = items[1].text
            else:
                group_name = items[0].text

            # 改行文字の数がものによって異なるため、一度改行文字を削除する
            clean_group_name = group_name.replace('\n', '')

            # ファイルに書き込む（改行文字を追加して）
            information_file.write(clean_group_name + '\n')
