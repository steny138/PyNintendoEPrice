用 Python 從網址下載zip檔案，並解壓縮後 解析成csv檔且讀取出來轉換成list

```
import requests
import csv
import io
from zipfile import ZipFile, ZIP_DEFLATED

with requests.Session() as s:
            r = s.get(rate_url)
            with ZipFile(io.BytesIO(r.content)) as thezip:
                for zipinfo in thezip.infolist():
                    with thezip.open(zipinfo) as thefile:
                        cr = csv.reader(thefile, delimiter=',', quotechar='"')
                        rate_csv_list = list(cr)
```