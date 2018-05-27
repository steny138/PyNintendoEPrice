# Google API 踩雷點

## 照官方範例得到以下錯誤
```
Traceback (most recent call last):
  File "google_sheet_pipline.py", line 24, in
    creds = store.get()
  File "/Users/YuChenMac/.virtualenvs/ns_web_crawler-wYNBDhQl/lib/python2.7/site-packages/oauth2client/client.py", line 407, in get
    return self.locked_get()
  File "/Users/YuChenMac/.virtualenvs/ns_web_crawler-wYNBDhQl/lib/python2.7/site-packages/oauth2client/file.py", line 54, in locked_get
    credentials = client.Credentials.new_from_json(content)
  File "/Users/YuChenMac/.virtualenvs/ns_web_crawler-wYNBDhQl/lib/python2.7/site-packages/oauth2client/client.py", line 302, in new_from_json
    module_name = data['_module']
KeyError: '_module'
```

原因是因為
因為他的憑證適用oauth2.0 而不是服務帳戶ServiceAccountCredentials

oauth2.0格式長這樣
```
{
    "_module": "oauth2client.client",
    "scopes": ["https://www.googleapis.com/auth/spreadsheets"],
    "token_expiry": "2018-05-27T10:25:38Z",
    "id_token": null,
    "user_agent": null,
    "access_token": "[Access Token]",
    "token_uri": "https://accounts.google.com/o/oauth2/token",
    "invalid": false,
    "token_response": {
        "access_token": "[Access Token]",
        "token_type": "Bearer",
        "expires_in": 3600,
        "refresh_token": "[Refresh Token]"
    },
    "client_id": "[Client ID].apps.googleusercontent.com",
    "token_info_uri": "https://www.googleapis.com/oauth2/v3/tokeninfo",
    "client_secret": "[Client Secret]",
    "revoke_uri": "https://accounts.google.com/o/oauth2/revoke",
    "_class": "OAuth2Credentials",
    "refresh_token": "[Refresh Token]",
    "id_token_jwt": null
}
```

service account 格式長這樣
```
{
  "type": "service_account",
  "project_id": "[project id]",
  "private_key_id": "[private_key_id]]",
  "private_key": "-----BEGIN PRIVATE KEY-----\n[THE PRIVATE KEY]\n-----END PRIVATE KEY-----\n",
  "client_email": "[The Service account]@.iam.gserviceaccount.com",
  "client_id": "[client_id]",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://accounts.google.com/o/oauth2/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/[Project ID].iam.gserviceaccount.com"
}

```

# Oauth 2.0

會先找有沒有 "_module" 的設定檔案如以下範例 credentials.json

若沒有 則用 從google api console抓下來的 client_secret.json 重新發起驗證

驗證通過會自動產生credentials.json

```
# Setup the Sheets API
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
```