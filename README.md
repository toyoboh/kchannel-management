## Kちゃんねる管理用ツール群

### 使用方法

### 補足

#### csvデータのインポート方法
データベースへはコマンドラインにてインポートする。
なお、以下の指定が必要。
- ファイル名（絶対パスもしくは相対パス）
- テーブル名
- 区切り文字（デフォルトではタブが区切り文字なので指定が必要）
- 囲み文字（今回は「"」）
- 先頭一行目を無視（CSVにはカラムも記載しているため）
```
MySQLに接続
mysql> use データベース名
mysql> LOAD DATA LOCAL INFILE "ファイル名" INTO TABLE テーブル名 FIELDS TERMINATED BY  "," OPTIONALLY ENCLOSED BY '"' OPTIONALLY IGNORE 1 LINES;
```
