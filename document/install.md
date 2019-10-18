
安裝sqlalchemy with postgre
需要依賴 DBAPI, postgre 預設為 psycopg2
而安裝psycopg2可能會有安裝依賴上的狀況
需用以下指令安裝即可.

```
env LDFLAGS='-L/usr/local/lib -L/usr/local/opt/openssl/lib
-L/usr/local/opt/readline/lib' pip install psycopg2
```

若Ｍac的Command Line Tools後發現無法成功安裝，得到下列訊息

> xcrun: error: invalid active developer path (/Library/Developer/CommandLineTools), missing xcrun at: /Library/Developer/CommandLineTools/usr/bin/xcrun
> 
>     It appears you are missing some prerequisite to build the package from source.
> 
>     You may install a binary package by installing 'psycopg2-binary' from PyPI.
>     If you want to install psycopg2 from source, please install the packages
>     required for the build and try again.
> 
>     For further information please check the 'doc/src/install.rst' file (also at
>     <http://initd.org/psycopg/docs/install.html>).
> 
>     error: command 'clang' failed with exit status 1

解決方式是在命令列下xcode-select --install後下載完就可以使用了。


因為後來爬網會遇到 Cloudflare 檢查是否為機器人
可參考 
https://github.com/Anorov/cloudflare-scrape/
跟
https://github.com/clemfromspace/scrapy-cloudflare-middleware
安裝Middleware來規避檢查機器人的方式，避免被鎖ＩＰ