
安裝sqlalchemy with postgre
需要依賴 DBAPI, postgre 預設為 psycopg2
而安裝psycopg2可能會有安裝依賴上的狀況
需用以下指令安裝即可.

```
env LDFLAGS='-L/usr/local/lib -L/usr/local/opt/openssl/lib
-L/usr/local/opt/readline/lib' pipenv install psycopg2
```


因為後來爬網會遇到 Cloudflare 檢查是否為機器人
可參考 
https://github.com/Anorov/cloudflare-scrape/
跟
https://github.com/clemfromspace/scrapy-cloudflare-middleware
安裝Middleware來規避檢查機器人的方式，避免被鎖ＩＰ