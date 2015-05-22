# libtanka is 何？
アセンブラ短歌をコンパイルなしでPythonを使って  
手軽に詠める・デバッグできるライブラリ。  
ノリと勢いで作ったものが人に使ってもらえるレベルになってきた  
・・・かもしれないので公開。  

# できること
Pythonだけで詠める
 * コンパイル→実行のめんどい流れが省略、やるだけ！

作った短歌をそのままSNSに貼り付けられる！
 * 実行時に短歌が5・7・5・7・7形式で出力される！

5・7・5・7・7であるかどうかのチェック
 * 機械語にどう翻訳されるか分からなくても大丈夫！
 * 脳内で変換しちゃうバイナリアンじゃなくても大丈夫！

他の人が詠んだ短歌をそのまま実行可能
 * もうバイナリエディタでコチコチやらなくていい！
 * ちゃんとアセンブラのニーモニックが表示される！
 
# できないこと
 短歌を作ることだけに特化してしまったので  
 短歌を作りながらバイナリファイルの成り立ちを勉強することはできません。  
 初めての人は、これで短歌を作ることに慣れたら  
 ぜひ、gccつかってコンパイルして、objdumpとかでコチコチやってみてください。  

# 使い方
* 短歌実行モジュール(tanka32)のビルド  
    `./configure CFLAGS='-g -O0';make  `

* 短歌実行モジュール(tanka32)の実行  
    `qira -s ./src/tanka32  `
  
* 短歌(サンプル)の詠み方  
    `chmod 755 ./bin/tanka.py`  
    `./bin/tanka.py`  

# API
libtanka.composeTanka(code)
* `code` :
	短歌のバイナリ(string)
* `返却値` :
	短歌の実行結果(string)
  
例：他の人が作った短歌を詠んでみる(サンプルの短歌は[坂井さんのページ](http://kozos.jp/asm-tanka/)から引用)

```python
import libtanka
import binascii

code = """
b8 57 61 6b 61
53 50 ba 04 00 00 00
bb 01 00 00 00
b8 04 00 00 00 89 e1
cd 80 58 31 c0 5b c3
"""
# ASCII -> binary
code = binascii.unhexlify(code.translate(None,' \n'))
result = libtanka.composeTanka(code)
print result
```

# 短歌を実行する仕組み
自分が作ったスクリプトが機械語をlibtankaに渡す  
→libtanka(機械語をqiraに渡す)  
→qira（機械語を受け取って、tanka32モジュールに標準入力から渡す）  
→tanka32モジュールが受け取って実行する(tanka.c)  
→その結果を標準出力に出す  
→qiraが受け取って、libtankaに渡す  
→libtankaが受け取る  
  
# 要求外部ライブラリ
アセンブルする時に必要  
[pwntools](https://github.com/Gallopsled/pwntools)  
機械語からニーモニックに変換する時に必要  
[capstone](https://github.com/aquynh/capstone)  
  
# 要求外部アプリケーション 
短歌をデバッグ・実行するときに必要  
[qira](https://github.com/BinaryAnalysisPlatform/qira)  

