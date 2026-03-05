# Data Parser Toolkit (OpenClaw)

這是一套針對「檔名混亂的Excel/CSV測試數據」進行自動化解析的 Python 工具集。
專為 **無法連網、無法安裝軟體、但有 Python 環境** 的公司內部電腦設計。

## 🎯 核心功能

*   **檔名解析**：自動從檔名中提取關鍵資訊 (如 `SN08`, `4.2V`, `55C`, `Cycle`, `Sanyo` 等)。
*   **欄位標準化**：將雜亂的檔名轉換為標準的 Excel 報表 (包含 Test Item, Sample ID, Condition, Vendor 等)。
*   **資料清理**：自動修正常見拼寫錯誤 (如 `Sanyo` vs `Sayno`)。
*   **輸出報表**：生成 `Parsed_Report_YYYYMMDD.xlsx`，可直接用於樞紐分析。

## 📦 安裝需求

請確保你的電腦已安裝 Python 3.6+。

### 1. 安裝依賴 (如果能連網)
```bash
pip install -r requirements.txt
```

### 2. 離線安裝 (如果不能連網)
請先在有網路的電腦下載 `.whl` 檔案，然後帶進公司：
```bash
pip install pandas-*.whl openpyxl-*.whl
```

## 🚀 使用方法

### 步驟 1：準備檔案
將所有要處理的 Excel/CSV 檔案放在一個資料夾中 (例如 `Z:\Test_Data\2023_Q4`)。

### 步驟 2：執行解析
打開 CMD (命令提示字元)，切換到本工具目錄，執行：

```bash
# 解析指定資料夾 (預設輸出到同一層目錄)
python parser_v3.py --input "Z:\Test_Data\2023_Q4"

# 指定輸出檔名
python parser_v3.py --input "Z:\Test_Data\2023_Q4" --output "My_Report.xlsx"
```

### 步驟 3：查看結果
程式執行完畢後，你會在目標資料夾看到一個新的 Excel 檔案，裡面包含了所有解析後的數據。

## 🛠️ 進階設定
你可以修改 `parser_v3.py` 中的 `KEYWORD_MAP` 字典，來新增或修改你的專屬關鍵字對應規則。

```python
# 例如新增一個供應商
KEYWORD_MAP = {
    # ...
    "molicel": "Molicel",
    "p45b": "Molicel",
    # ...
}
```

## 📝 版本紀錄
*   **v1.0 (2026-03-05)**: 初始版本，支援基礎檔名解析與 Excel 輸出。
