# ai_summary.py のテストコード
# 実行方法:
#    pytest tests/test_ai_summary.py -v

import pandas as pd
import pytest
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
def test_correct(monkeypatch):
    """DataFrameの統計情報がAIで要約され、文字列が返ること"""
    # テスト実行時だけ環境変数を上書き
    monkeypatch.setenv("GENAI_API_KEY", "dummy_key_for_test")
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
    monkeypatch.delenv("GENAI_API_KEY", raising=False)
    with pytest.raises(ValueError) as exc_info:
        summarize_dataframe(df)
    assert "GENAI_API_KEY" in str(exc_info.value)
 
def test_genai_generate_content_missing(monkeypatch):
    """AI要約の生成に失敗した場合、ConnectionErrorが発生すること"""
    monkeypatch.setenv("GENAI_API_KEY", "dummy_key")
    with pytest.raises(ConnectionError) as exc_info:
        summarize_dataframe(df)
    assert "AI要約" in str(exc_info.value)