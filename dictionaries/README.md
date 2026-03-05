# Dictionary Architecture (v2)

## Files
- `core_rules.v2.json`: 全測項共用規則（溫度、測項關鍵字、排除人名、RunVersion）
- `penetration_rules.v2.json`: 穿刺專用規則
- `merged_dictionary.v2.json`: 入口索引（global + 各測項路由 + 欄位優先順序）

## Why `CW(\d+)`
`CW(\d+)` 是正規表示式：
- `CW` = 固定前綴
- `(\d+)` = 抓取一段數字（1 位以上）

可匹配：`CW30`, `CW45`, `CW60` ...
比 `CW(30|45)` 更通用，避免每次新數值都要改字典。

## Next Step
當你提供加熱/過充/過放/外短的路徑檔名樣本後，依樣建立：
- `heating_rules.v2.json`
- `overcharge_rules.v2.json`
- `overdischarge_rules.v2.json`
- `ext_short_rules.v2.json`
