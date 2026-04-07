# 詳細設計書  

## 概要  
本設計書は詳細設計を記述する。  
※本設計書は学習目的のため、実装後に作成しています。  

---  

## 関数一覧  

| 関数名 | 所属ファイル | 概要 |
|--------|-------------|------|
| handle_error | utils.py | ログ記録後にエラーメッセージを表示し、処理を停止 |
| raise_error | utils.py  | ログ記録後に例外を発生 |
| load_data | app.py  | CSV読み込み |
| show_summary_stats | app.py   | 統計情報を表示する |
| compute_iqr_bounds | app.py  | IQR法で下限・上限の境界値を返す |
| detect_outliers | app.py  | IQR法で数値列の外れ値フラグを返す |
| build_highlight_styles | app.py  | 外れ値セルにCSSスタイルを付与したStylerを返す |
| apply_missing_strategy | app.py  | 欠損値を指定した方法で処理する |
| apply_outlier_strategy | app.py  | 外れ値を指定した方法で処理する |
| convert_df_to_csv | app.py  | DataFrameをCSVのバイト列に変換する |
| show_ai_summary | app.py  | AIによる要約を表示する |
| create_plot | app.py  | 選択された設定でグラフを作成して表示する |
| summarize_dataframe | ai_summary.py  | DataFrameの統計情報をAIで自動要約する |

---  

## 関数詳細  

### handle_error  

| 項目 | 内容 |
|------|------|
| 所属ファイル | utils.py |
| 概要 | ログ記録後にエラーメッセージを表示し、処理を停止 |
| 引数 | `user_message: str` ― ユーザー向け表示メッセージ |
|      | `ex_message: str` ― ログに記録する例外メッセージ |
|      | `log: bool = True` ― Falseの場合はログ記録をスキップ |
| 戻り値 | None |
| 例外 | 特になし |
| 備考 | 特になし |

処理内容  
１．logがTrueならば「表示メッセージ＋例外メッセージ」をログを記録する。  
２．ユーザーにユーザー向け表示メッセージを表示する。  
３．処理を停止する。  