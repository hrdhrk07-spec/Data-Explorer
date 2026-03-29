import os
import pandas as pd
from google import genai
from dotenv import load_dotenv

load_dotenv()

def summarize_dataframe(df: pd.DataFrame) -> str:
    """DataFrameの統計情報をAIで自動要約する"""
    # データの概要をテキスト化
    stats_text = f"""
    行数: {len(df)}行, 列数: {len(df.columns)}列
    カラム: {list(df.columns)}

    統計情報:
    {df.describe().to_string()}

    欠損値:
    {df.isnull().sum().to_string()}
    """

    client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""
            以下のCSVデータの統計情報を、ビジネスパーソン向けに
            3～5行で日本語で要約してください。
            重要な傾向、異常値、欠損データがあれば指摘してください。
            {stats_text}
        """
    )
    
    return response.text