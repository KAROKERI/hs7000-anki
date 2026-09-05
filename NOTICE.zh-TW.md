# 授權與著作權說明

[English](https://github.com/KAROKERI/hs7000-anki/blob/main/NOTICE.md) | **繁體中文**

本專案分成三層，授權方式各自不同，刻意保持分開，讓有著作權疑慮的那一
層永遠不需要離開你自己的電腦。

## 程式腳本（`scripts/`）-- MIT

`parse_ceec_pdf.py` 與 `build_apkg.py` 是原創程式碼，採用 MIT 授權
（見 `LICENSE`）。程式本身不含任何詞彙表內容——它們是你自己對自己
下載的 PDF 執行的工具。

## 卡片模板（`template/`）-- MIT

`template/card.css` 的 CSS 是為了這個純索引牌組而重新撰寫的原創內容。
它並未沿用或改編自任何第三方 Anki 牌組模板，因此採用與程式腳本
相同的 MIT 授權。

目前公開分享在 AnkiWeb 上的那份牌組，跟這裡的腳本產出的東西不一樣。它是直接從作者另一個獨立的個人「高中7000單字」學習牌組（內含完整中文釋義與兩句例句的那份）建置出來的，而不是用 `build_apkg.py` 產生的。那份個人牌組的卡片排版改編自 [egg rolls 的 JLPT10k 牌組](https://github.com/5mdld/anki-jlpt-decks)（CC BY-NC 4.0，非商業使用、需標註來源），這個署名已經標註在 AnkiWeb 的分享頁面上。如果你改用這個 repo 的腳本自己建置牌組，拿到的會是上面這份單純的 MIT 授權模板，不是改編自 egg rolls 的那份。

## 詞彙表內容 -- 未隨附，著作權屬大學入學考試中心 (CEEC)

本專案不隨附官方*高中英文參考詞彙表*（台灣大考中心的高中英文參考
詞彙表），也不隨附從中抽取的任何詞彙清單，或已建置好的 `.apkg`。該
詞彙表本身的著作權聲明寫道：
> 著作權屬財團法人大學入學考試中心基金會所有，僅供非營利目的使用，轉載請
> 註明出處。若作為營利目的使用，應事前經由財團法人大學入學考試中心基金會
> 書面同意授權。

（英文譯文："Copyright held by the CEEC Foundation. For non-commercial
use only; cite the source when reproducing it. Commercial use requires
prior written permission from the CEEC Foundation."）

要自行建置這份牌組，請下載你自己的官方 PDF 正本（在 ceec.edu.tw 搜尋
「高中英文參考詞彙表」，或見 `README.md` 中的直接連結），對你自己的
檔案執行 `scripts/parse_ceec_pdf.py` 以在本機產生 `words_by_level.json`，
再對這份 JSON 執行 `scripts/build_apkg.py`，產出你自己非營利用途的 `.apkg`。

PDF 原始檔、由它產生的 JSON、或已建置好的 `.apkg`，都不應該被提交到
本 repo 或從本 repo 再散布出去。
