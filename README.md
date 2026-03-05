# Data Parser Toolkit (OpenClaw)

這是一套針對「檔名混亂的 Excel/CSV 測試數據」進行自動化解析的 Python 工具。
專為公司內部電腦（有 Python、環境受限）設計。

## 🎯 核心功能
- 檔名解析：自動抽取關鍵資訊（如 SN08、4.2V、55C、Cycle、Sanyo）
- 欄位標準化：輸出結構化報表
- 資料清理：修正常見拼字變體
- 產出 Excel：方便後續樞紐分析

## 📦 安裝（一次就好）

```bash
python -m pip install -r requirements.txt
```

> 若 `pip` 指令找不到，請一律用 `python -m pip ...`

---

## 🚀 最簡單使用流程（Windows CMD）

### 1) 進入工具資料夾
```bat
cd /d "C:\Users\User\Downloads\data-parser-toolkit"
```

### 2) 解析一份檔案（CSV 或 TXT）
```bat
python parser_v3.py "C:\Users\User\Downloads\Test-052069.csv"
```

### 3) 指定輸出檔名（可選）
```bat
python parser_v3.py "C:\Users\User\Downloads\Test-052069.csv" "C:\Users\User\Downloads\parsed_output.xlsx"
```

---

## ⚠️ 常見錯誤

1. **`can't open file parser_v3.py`**
   - 你不在工具資料夾內。
   - 先 `cd /d "...\data-parser-toolkit"` 再執行。

2. **`only txt/csv supported`**
   - 目前僅支援 `.txt` 或 `.csv`。
   - 並且指令不要加 `--input`（本版本是位置參數）。

3. **`'pip' 不是內部或外部命令`**
   - 用：`python -m pip install -r requirements.txt`

---

## 🛠️ 字典擴充
你可以在 `parser_v3.py` 的對應字典區塊新增規則，提升命中率。

## 📝 版本紀錄
- **v1.1 (2026-03-05)**：修正 README 指令為可直接執行版本（移除 `--input` 旗標誤導）。
- **v1.0 (2026-03-05)**：初始版本。
