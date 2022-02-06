import sys
sys.path.append('../../../../')
from common.common import patterns_replace
import urllib.request
from bs4 import BeautifulSoup

# 抽出対象URL
url = 'https://www.pusannavi.com/special/5047301/index.html'

with urllib.request.urlopen(url) as req_file:
    # html解析
    html_file = req_file.read()
    soup      = BeautifulSoup(html_file, 'html.parser')

    # 料理名が入っているelementの取得
    food_elements     = soup.find_all(class_='atc_r_ttl')
    food_elements_num = len(food_elements)

    # 料理名を取り出し、txtファイルに書き込む
    with open('../data/information.txt', 'w') as list_file:
        for i in range(food_elements_num):
            # 料理名の抽出
            food_name = food_elements[i].text

            # 不要な文字列を取り除く
            clean_food_name = patterns_replace(food_name, [' ', '　'], "")
            
            # 最後の要素以外は改行文字をつける
            if i != food_elements_num -1:
                clean_food_name = clean_food_name + '\n'
            
            # テキストファイルに書き込む
            list_file.write(clean_food_name)
