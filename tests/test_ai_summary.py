# ai_summary.py のテストコード
# 実行方法:
#    pytest tests/test_ai_summary.py -v

import pandas as pd
import pytest
from unittest.mock import MagicMock, patch
from google import genai
from google.genai import errors
from ai_summary import summarize_dataframe

# テスト用のサンプルDataFrame
df = pd.DataFrame({
    "売上": [1000, 2000, None, 1500],
    "カテゴリ": ["食品", "雑貨", "食品", None],
    "数量": [3, None, 5, 2]
})

# 空のDataFrame
empty_df = pd.DataFrame()

# ------------------------------------------------------------------
# 正常系
# ------------------------------------------------------------------
def test_correct():
    """DataFrameの統計情報がAIで要約され、文字列が返ること"""
    summary = summarize_dataframe(df)

    assert isinstance(summary, str)
    assert len(summary) > 0
 
# ------------------------------------------------------------------
# 異常系
# ------------------------------------------------------------------ 
def test_dataframe_empty():
    """空のDataFrameが渡された場合、ValueErrorが発生すること"""
    with pytest.raises(ValueError) as exc_info:
        summarize_dataframe(empty_df)
    assert "DataFrame" in str(exc_info.value)

def test_api_key_missing(monkeypatch):
    """APIキーが環境変数に設定されていない場合、ValueErrorが発生すること"""
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    with pytest.raises(ValueError) as exc_info:
        summarize_dataframe(df)
    assert "GEMINI_API_KEY" in str(exc_info.value)
 
def test_generate_content_api_key_invalid(monkeypatch):
    """APIキーに誤りがある場合、ClientErrorが発生すること"""
    monkeypatch.setenv("GEMINI_API_KEY", "dummy_key")
    with pytest.raises(RuntimeError) as exc_info:
        summarize_dataframe(df)
    assert "API" in str(exc_info.value)

def test_generate_content_server_error():
    """サーバーエラーが発生した場合、ClientErrorが発生すること"""

    # clientのモックを作成
    mock_client = MagicMock()

    # generate_content を呼ぶと ServerError が発生するよう設定
    mock_client.models.generate_content.side_effect = errors.ServerError(
        500,
        {"error": {"code": 500, "message": "Internal error", "status": "INTERNAL"}},
    )

    # with文では__enter__の戻り値をモックに設定する必要がある
    mock_context = MagicMock()
    mock_context.__enter__ = MagicMock(return_value=mock_client)
    mock_context.__exit__ = MagicMock(return_value=False) # 例外を握り潰さない、省略可能

    # genai.Client(...)の戻り値をmock_clientに差し替える
    with patch("ai_summary.genai.Client", return_value=mock_context):
        with pytest.raises(RuntimeError) as exc_info:
            summarize_dataframe(df)
          
    assert "Internal" in str(exc_info.value)