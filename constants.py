# 定数とエラーメッセージを管理するモジュール
from enum import Enum

# 定数
AI_MODEL: str = "gemini-2.5-flash"
HIGHLIGHT_COLOR: str = "#cc4444"

# ログレベル
LOG_LEVEL_DEBUG = 10
LOG_LEVEL_INFO = 20
LOG_LEVEL_WARNING = 30
LOG_LEVEL_ERROR = 40

# エラーメッセージ
class ErrorMessage(Enum):
    CSV_EMPTY = "CSVファイルが空です。"
    CSV_PARSE_ERROR = "CSVファイルの形式が正しくありません。"
    CSV_LOAD_ERROR = "CSVの読み込みに失敗しました。"
    
    DF_EMPTY = "DataFrame が空のため要約できません。"
    API_KEY_MISSING = "GEMINI_API_KEYが環境変数に設定されていません。"
    AI_SUMMARY_FAILED = "AI要約の生成に失敗しました。"