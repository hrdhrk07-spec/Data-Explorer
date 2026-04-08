# 詳細設計書  

## 概要  
本設計書は詳細設計を記述する。  
※本設計書は学習目的のため、実装後に作成しています。  

---  

## 関数一覧  

| 関数名 | 所属ファイル | 概要 |
|--------|-------------|------|
| handle_error | utils.py | ログ記録後にエラーメッセージを表示し、処理を停止 |
| raise_error | utils.py | ログ記録後に例外を発生 |
| load_data | app.py | CSV読み込み |
| show_summary_stats | app.py | 統計情報を表示する |
| compute_iqr_bounds | app.py | IQR法で下限・上限の境界値を返す |
| detect_outliers | app.py | IQR法で数値列の外れ値フラグを返す |
| build_highlight_styles | app.py | 外れ値セルにCSSスタイルを付与したStylerを返す |
| apply_missing_strategy | app.py | 欠損値を指定した方法で処理する |
| apply_outlier_strategy | app.py | 外れ値を指定した方法で処理する |
| convert_df_to_csv | app.py | DataFrameをCSVのバイト列に変換する |
| show_ai_summary | app.py | AIによる要約を表示する |
| create_plot | app.py | 選択された設定でグラフを作成して表示する |
| summarize_dataframe | ai_summary.py | DataFrameの統計情報をAIで自動要約する |

---  

## 関数詳細  

### handle_error  

| 項目 | 内容 |
|------|------|
| 所属ファイル | utils.py |
| 概要 | ログ記録後にエラーメッセージを表示し、処理を停止 |
| 引数 | `user_message: str` ― 表示メッセージ |
|      | `ex_message: str` ― ログに記録する例外メッセージ |
|      | `log: bool = True` ― Falseの場合はログ記録をスキップ |
| 戻り値 | None |
| 例外 | なし |
| 備考 | なし |

処理内容  
１．logがTrueならば「表示メッセージ＋例外メッセージ」をログに記録する。  
２．ユーザーに「表示メッセージ」を表示する。  
３．処理を停止する。  

---  

### raise_error  

| 項目 | 内容 |
|------|------|
| 所属ファイル | utils.py |
| 概要 | ログ記録後に例外を発生 |
| 引数 | `log_level: int` ― ログレベル |
|      | `message: str` ― ログメッセージ |
|      | `error: Exception or None` ― 発生したエラー |
|      | `raise_as: type[Exception]` ― 発生させる例外 |
| 戻り値 | None |
| 例外 | なし |
| 備考 | ログレベル：DEBUG=10,INFO=20,WARNING=30,ERROR=40 |

処理内容  
１．ログレベルに応じて「ログメッセージ＋エラーメッセージ」をログに記録する。  
２．引数で指定した例外を発生させる。   

---  

### load_data  

| 項目 | 内容 |
|------|------|
| 所属ファイル | app.py |
| 概要 | CSV読み込み |
| 引数 | `file: UploadedFile` ― CSVファイル |
| 戻り値 | `pd.DataFrame` ― pandasの2次元データ構造 |
| 例外 | `EmptyDataError` ― 空データエラー |
|      | `ParserError` ― CSV形式エラー |
|      | `Exception` ― その他例外 |
| 備考 | なし |

処理内容  
１．pandasのCSV読み込みを実行する。  

例外発生時  
１．handle_error(表示用メッセージ,実際のエラーメッセージ)を呼び出す  
※発生した例外によってメッセージを変えること  

---  

### show_summary_stats  

| 項目 | 内容 |
|------|------|
| 所属ファイル | app.py |
| 概要 | 統計情報を表示する |
| 引数 | `df: pd.DataFrame` ― CSV読み込み後のデータ |
| 戻り値 | None |
| 例外 | なし |
| 備考 | なし |

処理内容  
１．streamlitのcolumns()を用いてページを2分割する。  
２．左側にpandasのDataFrame.describe()を用いて統計量を表示する。  
３．右側にpandasのDataFrame.isnull().sum()を用いて各列の欠損値の数を表示する。  

---  

### compute_iqr_bounds  

| 項目 | 内容 |
|------|------|
| 所属ファイル | app.py |
| 概要 | IQR法で下限・上限の境界値を返す |
| 引数 | `series: pd.Series` ― 各列のデータ（pandasの1次元データ） |
| 戻り値 | `tuple[float, float]` ― IQR法の下限、上限 |
| 例外 | なし |
| 備考 | なし |

処理内容  
１．データ群の中で25%点(Q1)のデータと75%点(Q3)のデータを取得する。  
２．IQR=Q3-Q1でIQR(四分位範囲)を計算する。  
３．下限:Q1-1.5×IQR、上限:Q3+1.5×IQRをそれぞれ計算し、値を返す。  

---  

### detect_outliers  

| 項目 | 内容 |
|------|------|
| 所属ファイル | app.py |
| 概要 | IQR法で数値列の外れ値フラグを返す |
| 引数 | `df: pd.DataFrame` ― CSV読み込み後のデータ |
| 戻り値 | `pd.DataFrame` ― 外れ値フラグ |
| 例外 | なし |
| 備考 | 引数と戻り値は同じデータ構造。外れ値のセルがTrue、それ以外がFalse。 |

処理内容  
１．引数と同じ形のDataFrameを作り、全てのセルをFalseで初期化する。  
２．引数のDataFrameの数値列のみを取り出し、列名一覧を取得する。  
    A.列ごとに繰り返し  
        A-1．compute_iqr_boundsを用いて列ごとにIQRの下限と上限を計算する。  
        A-2．下限または上限を外れたデータをTrueとするフラグを立てる。  
    繰り返し終了  
３．フラグを返す。  

---  

### build_highlight_styles  

| 項目 | 内容 |
|------|------|
| 所属ファイル | app.py |
| 概要 | 外れ値セルにCSSスタイルを付与したStylerを返す |
| 引数 | `df: pd.DataFrame` ― CSV読み込み後のデータ |
|      | `outlier_flags: pd.DataFrame` ― 外れ値フラグ |
|      | `missing_flags: pd.DataFrame` ― 欠損値フラグ |
| 戻り値 | `pd.Styler` ― pandasの表示専用レイヤー |
| 例外 | なし |
| 備考 | pd.StylerとはDataFrame を HTML/CSS で装飾するための仕組みのこと |
|      | df.style.apply() は「スタイルを返す関数」を行/列ごとに適用するメソッド |

処理内容  
１．関数を定義する。(ここでしか使わないため関数内で定義)  
    引数： col: pd.Series ― 各列  
    戻り値： list[str] ― リスト  
    処理：  
        A.列内の各セルで繰り返し  
            A-1.外れ値フラグがTrueの場合、外れ値のスタイルをリストに追加する  
            A-2.欠損値フラグがTrueの場合、欠損値のスタイルをリストに追加する  
        繰り返し終了  
        B.値を返す  

２．df.style.apply(定義した関数, axis=0)の結果を返す。  

---  

### apply_missing_strategy  

| 項目 | 内容 |
|------|------|
| 所属ファイル | app.py |
| 概要 | 欠損値を指定した方法で処理する |
| 引数 | `df: pd.DataFrame` ― CSV読み込み後のデータ |
|      | `strategy: str` ― 処理方法 |
| 戻り値 | `pd.DataFrame` ― 欠損値処理後のデータ |
| 例外 | なし |
| 備考 | 処理方法は4種類。処理しない、行ごと削除、数値を平均値で補完、数値を0で、文字列をMissingで補完 |

処理内容  
１．処理方法が「行ごと削除」の場合、DataFrame.dropna()で行を削除する。  
２．処理方法が「数値を平均値で補完」の場合  
    2-A.DataFrame.mean(numeric_only=True)で数値列のみ平均値を計算  
    2-B.DataFrame.fillna()で計算した平均値で補完する  
３．処理方法が「数値を0で、文字列をMissingで補完」の場合  
    3-A.数値列と文字列列に分ける  
    3-B.数値列はDataFrame.fillna(0)で補完する  
    3-C.文字列列はDataFrame.fillna("Missing")で補完する  
４．データを返す。  

---  

### apply_outlier_strategy  

| 項目 | 内容 |
|------|------|
| 所属ファイル | app.py |
| 概要 | 外れ値を指定した方法で処理する |
| 引数 | `df: pd.DataFrame` ― 欠損値処理後のデータ |
|      | `strategy: str` ― 処理方法 |
| 戻り値 | `pd.DataFrame` ― 欠損値・外れ値処理後のデータ |
| 例外 | なし |
| 備考 | 処理方法は3種類。処理しない、行ごと削除、数値を0で、IQRの上下限でクリップ |

処理内容  
１．処理方法が「行ごと削除」の場合  
    1-A.detect_outliers()を用いて外れ値フラグを取得  
    1-B.セルに外れ値が無い行を抽出し、DataFrame.reset_index()でインデックスを振り直す  
２．処理方法が「数値を0で、IQRの上下限でクリップ」の場合  
    2-A.数値列ごとに繰り返し  
        2-A-α.compute_iqr_bounds()を用いて列ごとにIQRの境界値を計算  
        2-A-β.下限を下回る値はlowerに、上限を上回る値はupperに置き換える  
    繰り返し終了   
３．データを返す。  

---  

### convert_df_to_csv  

| 項目 | 内容 |
|------|------|
| 所属ファイル | app.py |
| 概要 | DataFrameをCSVのバイト列に変換する |
| 引数 | `df: pd.DataFrame` ― 欠損値・外れ値処理後のデータ |
| 戻り値 | `bytes` |
| 例外 | なし |
| 備考 | なし |

処理内容  
１．DataFrame.to_csv()を用いてExcel対応のBOM付きUTF-8のバイト列に変換。  

---  

### show_ai_summary  

| 項目 | 内容 |
|------|------|
| 所属ファイル | app.py |
| 概要 | AIによる要約を表示する |
| 引数 | `df: pd.DataFrame` ― CSV読み込み後のデータ |
| 戻り値 | None |
| 例外 | `Exception` ― その他例外 |
| 備考 | 現状はCSV読み込み後のデータにのみ対応。加工済みデータには未対応。 |

処理内容  
１．streamlitで生成したボタンを押された場合  
    1-A.返答が返ってくるまで「AIがデータを分析中...」というメッセージを表示  
    1-B.summarize_dataframe()を呼び出して要約文を取得  
    1-C.取得した要約文を表示  

例外発生時  
１．handle_error(表示用メッセージ+実際のエラーメッセージ,"",log=False)を呼び出す  
※エラーはai_summary.pyでログに記録済みなので、ユーザーへの通知のみ。  
※AI要約の失敗時はユーザにもエラーメッセージを表示し、処理を停止する。  

---  

### create_plot  

| 項目 | 内容 |
|------|------|
| 所属ファイル | app.py |
| 概要 | 選択された設定でグラフを作成して表示する |
| 引数 | `df: pd.DataFrame` ― CSV読み込み後のデータ |
|      | `x: str` ― x軸の項目 |
|      | `y: str` ― y軸の項目 |
|      | `chart_type: ChartType` ― チャート形式 |
| 戻り値 | `pd.DataFrame` ― 外れ値フラグ |
| 例外 | なし |
| 備考 | チャート形式は3種類。散布図、棒グラフ、折れ線グラフ |

処理内容  
１．チャート形式が「散布図」の場合、plotly.express.scatter()で散布図を設定  
２．チャート形式が「棒グラフ」の場合、plotly.express.scatter()で棒グラフを設定  
３．チャート形式が「折れ線グラフ」の場合、plotly.express.scatter()で折れ線グラフを設定  
４．streamlit.plotly_chat()でグラフを表示  

---

### summarize_dataframe  

| 項目 | 内容 |
|------|------|
| 所属ファイル | app.py |
| 概要 | DataFrameの統計情報をAIで自動要約する |
| 引数 | `df: pd.DataFrame` ― pandasの2次元データ構造 |
| 戻り値 | `str` ― 要約文 |
| 例外 | `google.genai.ClientError` ― クライアントエラー |
|      | `google.genai.ServerError` ― サーバーエラー |
|      | `google.genai.ClientError` ― その他例外 |
| 備考 | Google Gemini API（gemini-2.5-flash）を使用 |

処理内容  
１．引数のデータが空の場合、raise_error()で例外を発生する。  
    ログレベルはWARNING、例外はValueErrorを設定  
２．環境変数からAPIキーを取得する。  
３．APIキーが空の場合、raise_error()で例外を発生する。  
    ログレベルはERROR、例外はValueErrorを設定  
４．AIに渡すプロンプトを作成する。  
※対応する数字や文字列はf文字列で適宜埋めていくこと  

↓プロンプトここから  
以下のCSVデータの統計情報を、ビジネスパーソン向けに  
3～5行で日本語で要約してください。  
重要な傾向、異常値、欠損データがあれば指摘してください。  
行数：○行、列数：×列  
カラム：xx,yy.....  
統計情報：DataFrame.describe().to_string()  
欠損値：DataFrame.isnull().sum().to_string()  
↑プロンプトここまで  

５．genai.Client()でクライアントを初期化する。  
６．client.models.generate_content()でAPIを呼び出す。  
    generate_contentの引数は以下の通り  
    model="gemini-2.5-flash",  
    contents=作成したプロンプト  
７．戻ってきた要約文を返す。  

例外発生時  
１．raise_error()で例外を発生する  
    ログレベルはERROR、例外はRunTimeErrorを設定  
※発生した例外によってメッセージを変えること  