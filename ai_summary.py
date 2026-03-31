import os
import pandas as pd
from constants import LOG_LEVEL_WARNING, LOG_LEVEL_ERROR, AI_MODEL, ErrorMessage
from utils import raise_error
from google import genai
from google.genai import errors
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

# 関数
def summarize_dataframe(df: pd.DataFrame) -> str:
    """DataFrameの統計情報をAIで自動要約する"""

    # 引数のデータが空であるかを確認
    if df.empty:
        raise_error(LOG_LEVEL_WARNING, ErrorMessage.DF_EMPTY.value, None, ValueError)

    # APIキーの取得
    gemini_api_key: str = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise_error(LOG_LEVEL_ERROR, ErrorMessage.API_KEY_MISSING.value, None, ValueError)

    # データの概要をテキスト化
    stats_text = f"""
    行数: {len(df)}行, 列数: {len(df.columns)}列
    カラム: {list(df.columns)}

    統計情報:
    {df.describe().to_string()}

    欠損値:
    {df.isnull().sum().to_string()}
    """
    
    # ここではClientクラスを初期化しているだけでまだAPIを叩いていない。
    # 主な失敗要因であるAPIキーが空のケースは事前に弾いているためtry-exceptで囲む必要なしと判断。
    with genai.Client(api_key = gemini_api_key) as client:
        try:
            response = client.models.generate_content(
                model = AI_MODEL,
                contents = f"""
                以下のCSVデータの統計情報を、ビジネスパーソン向けに
                3～5行で日本語で要約してください。
                重要な傾向、異常値、欠損データがあれば指摘してください。
                {stats_text}
                """
            )
        except errors.ClientError as e:
            # API_KEYの誤り、通信エラーやAPIの使用制限などモデルやクライアント側の問題
            # エラー内容はGOOGLE依存であるため、ユーザにも直接見せるように設定
            raise_error(LOG_LEVEL_ERROR, str(e), None, RuntimeError)
        except errors.ServerError as e:
            # サーバー側の問題
            raise_error(LOG_LEVEL_ERROR, str(e), None, RuntimeError)
        except Exception as e:
            # その他の予期せぬエラー
            raise_error(LOG_LEVEL_ERROR, str(e), None, RuntimeError)

    return response.text