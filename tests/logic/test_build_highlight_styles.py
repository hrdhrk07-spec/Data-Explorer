# 関数 build_highlight_styles() のテストコード
# 実行方法:
#    pytest  tests/logic/test_build_highlight_styles.py

import pandas as pd
import pytest
import re
from constants import HIGHLIGHT_OUTLIER, HIGHLIGHT_MISSING
from app import build_highlight_styles

# フィクスチャ
@pytest.fixture
def test_df() -> pd.DataFrame:
    """テスト用のサンプルDataFrame"""
    return pd.DataFrame({"price": [100, 9999, None]})

@pytest.fixture
def outlier_flags() -> pd.DataFrame:
    """テスト用の外れ値フラグDataFrame"""
    return pd.DataFrame({"price": [False, True, False]})

@pytest.fixture
def missing_flags() -> pd.DataFrame:
    """テスト用の欠損値フラグDataFrame"""
    return pd.DataFrame({"price": [False, False, True]})


# ------------------------------------------------------------------
# 正常系
# ------------------------------------------------------------------
def test_build_highlight_styles_applies_color_to_flagged_cell(test_df, outlier_flags, missing_flags):
    """外れ値と欠損値のTrueフラグのセルにハイライトが付与される"""
    styled = build_highlight_styles(test_df, outlier_flags, missing_flags)
    
    # styled.to_html() で生成するHTMLを取得
    html = styled.to_html()
    
    # ハイライトが付与されたセルのCSSスタイルを正規表現で抽出して確認
    css_block_outlier = re.search(r"#T_\w+_row1_col0\s*\{([^}]+)\}", html)
    css_block_missing = re.search(r"#T_\w+_row2_col0\s*\{([^}]+)\}", html)

    # 抽出した文字列が空でないことを確認後、背景色のスタイルが含まれていることを確認
    assert css_block_outlier is not None
    assert f"background-color: {HIGHLIGHT_OUTLIER}" in css_block_outlier.group(1) # group(0)はマッチ全体、group(1)でCSSプロパティの部分を取得
    assert css_block_missing is not None
    assert f"background-color: {HIGHLIGHT_MISSING}" in css_block_missing.group(1)


def test_build_highlight_styles_no_color_for_unflagged_cell(test_df, outlier_flags, missing_flags):
    """Falseフラグのセルにはハイライトが付与されない"""
    styled = build_highlight_styles(test_df, outlier_flags, missing_flags)
    
    # styled.to_html() で生成するHTMLを取得
    html = styled.to_html()
    
    # ハイライトが付与されたセルのCSSスタイルを正規表現で抽出して確認
    css_block = re.search(r"#T_\w+_row0_col0\s*\{([^}]+)\}", html)
    
    # Falseフラグのセルはスタイルが付与されないため空文字となることを確認
    assert css_block is None