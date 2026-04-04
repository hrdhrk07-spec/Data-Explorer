# 定数とエラーメッセージを管理するモジュール
from enum import Enum

# 定数
AI_MODEL: str = "gemini-2.5-flash"
HIGHLIGHT_OUTLIER: str = "#E0AC00"
HIGHLIGHT_MISSING: str = "#cc4444"


# ログレベル
LOG_LEVEL_DEBUG = 10
LOG_LEVEL_INFO = 20
LOG_LEVEL_WARNING = 30
LOG_LEVEL_ERROR = 40

# ドロップダウンの選択肢
class Dropdown_Missing(Enum):
    PROCESS_NONE = "処理しない"
    ROW_DROP = "行ごと削除"
    MEAN_FILL = "数値を平均値で補完"
    ZERO_FILL = "数値を0で、文字列をMissingで補完"

class Dropdown_Outlier(Enum):
    PROCESS_NONE = "処理しない"
    ROW_DROP = "行ごと削除"
    IQR_CLIP = "IQRの上下限でクリップ"

# エラーメッセージ
class ErrorMessage(Enum):
    CSV_EMPTY = "CSVファイルが空です。"
    CSV_PARSE_ERROR = "CSVファイルの形式が正しくありません。"
    CSV_LOAD_ERROR = "CSVの読み込みに失敗しました。"
    
    DF_EMPTY = "空データのため要約できません。"
    API_KEY_MISSING = "GEMINI_API_KEYが環境変数に設定されていません。"
    AI_SUMMARY_FAILED = "AI要約の生成に失敗しました。"