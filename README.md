# Google Play Web Crawler

Google Play Web Crawler是一個用於自動檢查指定 Android 應用在 Google Play 上的最新版本的 Python 腳本。該腳本使用 `pyppeteer` 庫模擬瀏覽器行為，以便於抓取和解析應用版本信息。

## 特點

- 通過 `config.ini` 配置檔案，輕鬆管理需要檢查的應用列表。
- 支持自動讀取和寫入應用的當前版本信息到本地檔案。
- 通過日誌記錄操作過程，便於問題追蹤和調試。

## 環境需求

- Python 3.7+
- pyppeteer

## 安裝依賴

在安裝腳本依賴前，請確保您的 Python 環境已正確設置。使用以下命令安裝所需的 Python 庫：

```bash
pip install pyppeteer
```
---ini----
[apps]
MOMO = https://play.google.com/store/apps/details?id=com.mservice.momotransfer

[selectors]
button_selector = 你的按鈕選擇器
version_selector = 你的版本選擇器

[paths]
versions_file = versions.txt



使用方法
確保配置檔案 config.ini 已正確設置後，運行腳本：

'''bash

python CheckVersion_2.py
```
腳本將根據配置檔案中的信息檢查每個應用的版本，如有更新，將更新信息寫入指定的本地檔案中。

日誌
腳本運行過程中的信息將通過日誌形式輸出，幫助追蹤操作過程及調試。
