# 関数 detect_outliers() のテストコード
# 実行方法:
#    pytest  tests/logic/test_detect_outliers.py

import pandas as pd
import pytest
from app import detect_outliers


# フィクスチャ
@pytest.fixture
def normal_df() -> pd.DataFrame:
    """外れ値なしの正常データ"""
    return pd.DataFrame({
        "price": [100, 110, 105, 95, 108],
        "quantity": [10, 12, 11, 9, 13],
    })


@pytest.fixture
def outlier_df() -> pd.DataFrame:
    """明確な外れ値を1件含むデータ"""
    return pd.DataFrame({
        "price": [100, 110, 105, 95, 9999],  # 9999が外れ値
        "quantity": [10, 12, 11, 9, 13],
    })


@pytest.fixture
def non_numeric_df() -> pd.DataFrame:
    """数値列と文字列列が混在するデータ"""
    return pd.DataFrame({
        "name": ["田中", "佐藤", "鈴木", "近藤", "高橋"],
        "price": [100, 110, 105, 95, 9999],
    })


# ------------------------------------------------------------------
# 正常系
# ------------------------------------------------------------------
def test_no_outliers(normal_df):
    """外れ値なしのデータではすべてFalseになる"""
    result = detect_outliers(normal_df)
    assert not result.any().any()


def test_outlier_detected(outlier_df):
    """明確な外れ値が正しく検出される"""
    result = detect_outliers(outlier_df)
    assert result["price"].iloc[4] == True  # 9999 の行


def test_non_outlier_cells_are_false(outlier_df):
    """外れ値でないセルはFalseのまま"""
    result = detect_outliers(outlier_df)
    assert not result["price"].iloc[:3].any()


def test_non_numeric_columns_are_false(non_numeric_df):
    """文字列列はすべてFalseになる"""
    result = detect_outliers(non_numeric_df)
    assert not result["name"].any()


def test_output_shape_matches_input(outlier_df):
    """返り値のshape(行数・列数)が入力と一致する"""
    result = detect_outliers(outlier_df)
    assert result.shape == outlier_df.shape


def test_output_dtype_is_bool(outlier_df):
    """返り値のDTypeがboolである"""
    result = detect_outliers(outlier_df)
    assert all(result[col].dtype == bool for col in result.columns)


def test_empty_dataframe():
    """空のDataFrameでもエラーにならない"""
    empty = pd.DataFrame()
    result = detect_outliers(empty)
    assert result.empty