import sys
sys.path.append('../../../../')
from common.common import patterns_replace
import urllib.request
from bs4 import BeautifulSoup
import requests

# 抽出対象URL
url = 'https://www.pusannavi.com/special/5047301/index.html'

# 料理名を格納する配列
food_list = []

# 対象URLにアクセスしデータを取得およびhtml解析
res_data = requests.get(url)
res_data.encoding = res_data.apparent_encoding # 文字化け対策
soup = BeautifulSoup(res_data.text, 'html.parser')

# 料理名が入っている全部の要素（タグ）取得
food_elements = soup.find_all(class_='atc_r_ttl')

# 取得された要素から料理名を取得（不要な文字は取り除く）し、料理名配列に格納する
for element in food_elements:
    food_name = element.text
    clean_food_name = patterns_replace(food_name, [' ', '　', '\n'], '')

    food_list.append(clean_food_name)

# ファイルに料理名を書き込む
with open('../data/information.txt', 'w') as information_file:
    food_list_num       = len(food_list)    # 配列要素数を取得
    list_last_index_num = food_list_num - 1 # 配列の最後のインデックス番号を取得

    for i in range(food_list_num):
        # 配列の最後の料理名以外は、改行文字を後ろにつける
        if i == list_last_index_num:
            information_file.write(food_list[i])
        else:
            information_file.write(food_list[i] + '\n')
