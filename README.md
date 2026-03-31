## 概要:  
アップロードしたCSVデータを即座に可視化・分析するためのWebアプリケーションです。  
現在、エラー制御の改善中及びテストコードの作成中です。  

サンプルデータは data/ にあります。  
データの再生成は scripts/ 下のスクリプトで可能です。  

## なぜこれを作ったか:  
実務のブランクを鑑み、バックエンド処理を中心にしながら近年主流の言語であるPythonを学習するために作成しています。    

## 機能:  
- CSVファイルのアップロードと即時プレビュー  
- 統計情報の自動表示（平均・中央値・標準偏差など）  
- インタラクティブなグラフ可視化（Plotly）  
- AIによるデータ自動要約（Google Gemini API）  
- 欠損値・異常値の検出と表示  
- エラー発生時のログ出力  

## こだわった点:
・エラーハンドリングの徹底: 業務では必須となるエラーハンドリングをログ出力含め実装しています。  
・保守性の向上: 定数をconstants.py、汎用関数をutils.pyにまとめ、型ヒントの有無に気を付けてチーム開発を想定した可視性の高いコードを記述しました。  
・テストの自動化: pytestを用いたテストコードを作成し、テストの自動化を実装しています。   

## 使用技術:  
| カテゴリ | 技術 |  
|---|---|  
| フロントエンド | Streamlit |  
| データ処理 | Pandas |  
| 可視化 | Plotly |  
| AI要約 | Google Gemini API（gemini-2.5-flash）|  
| 環境変数管理 | python-dotenv |  
| テスト | pytest |  
| 言語 | Python 3.11+ |  

## セットアップ手順:  
### 1. リポジトリのクローン  
git clone https://github.com/hrdhrk07-spec/smart-data-explorer.git  
cd data-explorer  

### 2. ライブラリのインストール  
pip install -r requirements.txt  

### 3. APIキーの設定 ← 追加セクション  
AI要約機能にはGoogle Gemini APIキーが必要です。  

1. [Google AI Studio](https://aistudio.google.com) にアクセス  
2. Googleアカウントでログインし、APIキーを発行  
3. プロジェクトルートに`.env`ファイルを作成し、以下を記載：  

GEMINI_API_KEY=your_api_key_here  

> ⚠️ `.env`ファイルは`.gitignore`により管理対象外です。  

### 4. アプリの起動  
streamlit run app.py  

## ⚠️ 注意事項  
- AI要約機能はGoogle Gemini APIの**無料枠**で十分使用可能です  
- APIキーなしでも、AI要約機能以外はすべて動作します  
- `.env`ファイルは`.gitignore`で除外済みのため、クローン後に別途作成が必要です  
