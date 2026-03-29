import os
import pandas as pd
from google import genai
from dotenv import load_dotenv
from logger import setup_logger

# 環境変数の読み込み    
load_dotenv()

# ログ設定
logging = setup_logger()

# 関数
def summarize_dataframe(df: pd.DataFrame) -> str:
    """DataFrameの統計情報をAIで自動要約する"""

    # APIキーの取得
    gemini_api_key: str = os.getenv("GENAI_API_KEY")
    if not gemini_api_key:
        logging.error("GENAI_API_KEYが環境変数に未設定")
        raise ValueError("GENAI_API_KEYが環境変数に設定されていません。")

    # データの概要をテキスト化
    stats_text = f"""
    行数: {len(df)}行, 列数: {len(df.columns)}列
    カラム: {list(df.columns)}

    統計情報:
    {df.describe().to_string()}

    欠損値:
    {df.isnull().sum().to_string()}
    """

    try:
        client = genai.Client(api_key = gemini_api_key)
    except Exception as e:
        logging.error(f"AIクライアントの初期化に失敗: {e}")
        raise ConnectionError(f"AIクライアントの初期化に失敗しました: {e}")
    
    try:
        response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""
            以下のCSVデータの統計情報を、ビジネスパーソン向けに
            3～5行で日本語で要約してください。
            重要な傾向、異常値、欠損データがあれば指摘してください。
            {stats_text}
        """
        )
    except Exception as e:
        logging.error(f"AI要約の生成に失敗: {e}")   
        raise RuntimeError(f"AI要約の生成に失敗しました: {e}")
    
    return response.text