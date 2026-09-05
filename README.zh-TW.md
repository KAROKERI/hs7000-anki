# hs7000-anki

[English](https://github.com/KAROKERI/hs7000-anki/blob/main/README.md) | **繁體中文**

將台灣大學入學考試中心《高中英文參考詞彙表》轉換為 Anki 牌組的工具，依
Level 1-6 整理成同一個 `.apkg` 內的子牌組——採用與 [egg rolls JLPT10k 牌組](https://github.com/5mdld/anki-jlpt-decks) 相同的「單一牌組、內部依級分層」架構（該牌組用這種方式整理 N1-N5）。

本專案不隨附任何詞彙表內容——僅提供解析與建置工具。原因與完整的授權
說明請見 `NOTICE.zh-TW.md`。

不想自己跑腳本嗎？做好的牌組已公開分享在 AnkiWeb： [高中英文參考詞彙表 Level 1-6（111學年度起適用｜含中譯例句）](https://ankiweb.net/shared/info/996501688)。跟下面腳本產出的內容不一樣，AnkiWeb 上那份含有中文釋義與每張卡兩句例句，因為它是直接從作者自己的個人學習牌組建置出來的，不是用這裡的腳本產生——套用的模板授權也不同，詳見 `NOTICE.zh-TW.md`。直接匯入 Anki 桌面版即可使用，不需要 PDF，也不需要跑 Python。這個 repo 本身仍然只提供程式腳本。

## 卡片內容

每張卡片：正面是英文單字，背面是詞性加上官方級別（`Level 1` 到 `Level 6`）。這是單純的詞彙索引，不是完整學習牌組——不含中文釋義或
例句，因為官方詞彙表本身也沒有這些內容。（這說的是這個 repo 的腳本會建置出來的東西。上面連結的 AnkiWeb 現成牌組不一樣、內容更豐富，詳見 `NOTICE.zh-TW.md`。）

## 使用方式

安裝相依套件：

```bash
pip install pdfplumber genanki
```

到 CEEC 官網下載你自己的官方 PDF 正本（在 ceec.edu.tw 搜尋 `高中英文參考詞彙表`），然後解析成詞彙 JSON 並建置 `.apkg`：

```bash
python3 scripts/parse_ceec_pdf.py your-copy.pdf -o words_by_level.json
python3 scripts/build_apkg.py words_by_level.json -o hs7000-level1-6.apkg
```

之後把 `hs7000-level1-6.apkg` 匯入 Anki，會得到一個主牌組，底下六個
子牌組 `Level 1` 到 `Level 6`。

## 解析驗證

對照 111學年度起適用版本：6,012 筆詞條，每級恰好 1,002 筆，0 個重複
詞條，經過欄位感知的 PDF 文字重建後 0 筆未解析殘留（PDF「依字母排序」
章節是三欄式排版，naive 的 `pdftotext` 式擷取會把欄位順序打亂——解析
器如何還原正確閱讀順序，詳見程式內的說明文件）。這與 PDF 原文所述設計
相符（「每一級收錄約1,000詞條，六個級別共計約6,000詞條」）。若解析
不同版本得到差異很大的總數，用 `--debug-columns` 重新檢查欄位座標是否
仍符合該版本的排版。

## 授權

`scripts/` 與 `template/` 採用 MIT 授權（見 `LICENSE`）。詞彙表內容未
隨附——著作權屬 CEEC，詳見 `NOTICE.zh-TW.md`。
# hs7000-anki

[English](README.md) | **繁體中文**

將台灣大學入學考試中心《高中英文參考詞彙表》轉換為 Anki 牌組的工具，依
Level 1-6 整理成同一個 `.apkg` 內的子牌組——採用與
[egg rolls JLPT10k 牌組](https://github.com/5mdld/anki-jlpt-decks)
相同的「單一牌組、內部依級分層」架構（該牌組用這種方式整理 N1-N5）。

本專案不隨附任何詞彙表內容——僅提供解析與建置工具。原因與完整的授權
說明請見 `NOTICE.zh-TW.md`。

不想自己跑腳本嗎？做好的牌組已公開分享在 AnkiWeb：
[高中英文參考詞彙表 Level 1-6（111學年度起適用｜含中譯例句）](https://ankiweb.net/shared/info/996501688)。
直接匯入 Anki 桌面版即可使用，不需要 PDF，也不需要跑 Python。這個 repo
本身仍然只提供程式腳本——原因見 `NOTICE.zh-TW.md`。

## 卡片內容

每張卡片：正面是英文單字，背面是詞性加上官方級別（`Level 1` 到
`Level 6`）。這是單純的詞彙索引，不是完整學習牌組——不含中文釋義或
例句，因為官方詞彙表本身也沒有這些內容。

## 使用方式

安裝相依套件：

```bash
pip install pdfplumber genanki
```

到 CEEC 官網下載你自己的官方 PDF 正本（在 ceec.edu.tw 搜尋
`高中英文參考詞彙表`），然後解析成詞彙 JSON 並建置 `.apkg`：

```bash
python3 scripts/parse_ceec_pdf.py your-copy.pdf -o words_by_level.json
python3 scripts/build_apkg.py words_by_level.json -o hs7000-level1-6.apkg
```

之後把 `hs7000-level1-6.apkg` 匯入 Anki，會得到一個主牌組，底下六個
子牌組 `Level 1` 到 `Level 6`。

## 解析驗證

對照 111學年度起適用版本：6,012 筆詞條，每級恰好 1,002 筆，0 個重複
詞條，經過欄位感知的 PDF 文字重建後 0 筆未解析殘留（PDF「依字母排序」
章節是三欄式排版，naive 的 `pdftotext` 式擷取會把欄位順序打亂——解析
器如何還原正確閱讀順序，詳見程式內的說明文件）。這與 PDF 原文所述設計
相符（「每一級收錄約1,000詞條，六個級別共計約6,000詞條」）。若解析
不同版本得到差異很大的總數，用 `--debug-columns` 重新檢查欄位座標是否
仍符合該版本的排版。

## 授權

`scripts/` 與 `template/` 採用 MIT 授權（見 `LICENSE`）。詞彙表內容未
隨附——著作權屬 CEEC，詳見 `NOTICE.zh-TW.md`。
