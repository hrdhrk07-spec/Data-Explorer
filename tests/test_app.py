# app.py のテストコード
# 実行方法:
#    pytest tests/test_app.py -v
 
import io
import pytest
import pandas as pd
from app import compute_iqr_bounds, convert_df_to_csv, detect_outliers, apply_outlier_strategy, apply_missing_strategy
from constants import Dropdown_Missing, Dropdown_Outlier

# フィクスチャ
@pytest.fixture
def test_df() -> pd.DataFrame:
    """テスト用DataFrame"""
    return pd.DataFrame({
        "売上": [1000, 2000, None, 1500, 3000, 50000, -9999],  # 50000, -9999は明らかな外れ値
        "カテゴリ": ["食品", "雑貨", "食品", None, "雑貨", "食品", "雑貨"],
        "数量": [3, None, 5, 2, 4, 1, 6]
    })

# ------------------------------------------------------------------
# ヘルパー: 文字列からファイルオブジェクトを作る
# io.StringIO を使うと、実際のファイルなしにCSV文字列をテストできる
# ------------------------------------------------------------------
 
def make_csv(content: str) -> io.StringIO:
    """CSV文字列 → ファイルオブジェクト（テスト用）"""
    return io.StringIO(content)

# ------------------------------------------------------------------
# 正常系
# ------------------------------------------------------------------
def test_reads_basic_csv():
    """通常のCSVが正しく読み込めること"""
    csv = make_csv("sales,quantity\n1000,10\n2000,20")
    df = pd.read_csv(csv)
 
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["sales", "quantity"]
    assert len(df) == 2
 
def test_correct_values():
    """値が正しく読み込まれること"""
    csv = make_csv("売上,数量\n1000,10\n2000,20")
    df = pd.read_csv(csv)
 
    assert df["売上"].iloc[0] == 1000
    assert df["数量"].iloc[1] == 20
 
def test_missing_values():
    """欠損値（空セル）を含むCSVが読み込めること"""
    csv = make_csv("sales,product\n1000,A\n,B\n3000,")
    df = pd.read_csv(csv)
 
    # 欠損値は NaN になるはず
    assert df["sales"].isna().sum() == 1
    assert df["product"].isna().sum() == 1

def test_single_row():
    """1行だけのCSVが読み込めること"""
    csv = make_csv("sales\n500")
    df = pd.read_csv(csv)
 
    assert len(df) == 1
    assert df["sales"].iloc[0] == 500

def test_compute_iqr_bounds():
    """境界値が正しく計算されること。"""
    s = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0])
    lower, upper = compute_iqr_bounds(s)
    q1, q3 = s.quantile(0.25), s.quantile(0.75)
    iqr = q3 - q1
    assert lower == q1 - 1.5 * iqr
    assert upper == q3 + 1.5 * iqr

def test_convert_df_to_csv(test_df):
    """DataFrameが正しくBOM付きUTF-8のCSVに変換されること"""
    result = convert_df_to_csv(test_df)
    assert isinstance(result, bytes)
    # BOM付きUTF-8の確認
    assert result.startswith(b"\xef\xbb\xbf")
    # ヘッダーが含まれているか確認
    decoded = result.decode("utf-8-sig")
    for col in test_df.columns:
        assert col in decoded

def test_apply_missing_strategy_none(test_df):
    """欠損値を処理しない場合、DataFrameが変わらないこと。"""
    result = apply_missing_strategy(test_df, Dropdown_Missing.PROCESS_NONE.value)
    assert test_df.equals(result)

def test_apply_missing_strategy_drop(test_df):
    """欠損値を含む行が削除されること。"""
    result = apply_missing_strategy(test_df, Dropdown_Missing.ROW_DROP.value)
    assert result.isnull().sum().sum() == 0

def test_apply_missing_strategy_mean(test_df):
    """数値列の欠損値が平均値で補完されること。"""
    # 補完前に各列の平均値を計算しておく
    expected_means = test_df.mean(numeric_only=True)
    result = apply_missing_strategy(test_df, Dropdown_Missing.MEAN_FILL.value)
    for col in test_df.select_dtypes(include="number").columns:
        missing_mask = test_df[col].isnull()
        if missing_mask.any():
            # 欠損だった箇所が平均値になっているか確認
            assert (result.loc[missing_mask, col] == expected_means[col]).all()

def test_apply_missing_strategy_zero(test_df):
    """数値列は0、文字列列は'Missing'で補完されること。"""
    result = apply_missing_strategy(test_df, Dropdown_Missing.ZERO_FILL.value)

    # 数値列：欠損がなく、0で補完されている
    for col in result.select_dtypes(include="number").columns:
        assert result[col].isnull().sum() == 0
        # 元データに欠損があった箇所が0になっているか確認
        missing_mask = test_df[col].isnull()
        assert (result.loc[missing_mask, col] == 0).all()

    # 文字列列：欠損がなく、"Missing"で補完されている
    for col in result.select_dtypes(include="object").columns:
        assert result[col].isnull().sum() == 0
        missing_mask = test_df[col].isnull()
        assert (result.loc[missing_mask, col] == "Missing").all()

def test_apply_outlier_strategy_none(test_df):
    """外れ値を処理しない場合、DataFrameが変わらないこと。"""
    result = apply_outlier_strategy(test_df, Dropdown_Outlier.PROCESS_NONE.value)
    assert test_df.equals(result)

def test_apply_outlier_strategy_drop(test_df):
    """外れ値を含む行が削除されること。"""
    result = apply_outlier_strategy(test_df, Dropdown_Outlier.ROW_DROP.value)
    outlier_flags = detect_outliers(result)
    assert outlier_flags.any(axis=1).sum() == 0

def test_apply_outlier_strategy_clip(test_df):
    """外れ値がIQRの上限・下限にクリッピングされること。"""
    result = apply_outlier_strategy(test_df, Dropdown_Outlier.IQR_CLIP.value)

    for col in test_df.select_dtypes(include="number").columns:
        # compute_iqr_boundsが正しい前提でテストしているので注意
        lower, upper = compute_iqr_bounds(test_df[col])
        outlier_mask = (test_df[col] < lower) | (test_df[col] > upper)
        if outlier_mask.any():
            # 下限未満だった箇所がlowerになっているか確認
            lower_mask = test_df[col] < lower
            if lower_mask.any():
                assert (result.loc[lower_mask, col] == lower).all()
            # 上限超過だった箇所がupperになっているか確認
            upper_mask = test_df[col] > upper
            if upper_mask.any():
                assert (result.loc[upper_mask, col] == upper).all()

# ------------------------------------------------------------------
# 異常系
# ------------------------------------------------------------------ 
def test_empty_file_raises():
    """空ファイルは pd.errors.EmptyDataError になること"""
    csv = make_csv("") # 空文字列は空ファイルと同じ
 
    with pytest.raises(pd.errors.EmptyDataError):
        pd.read_csv(csv)

def test_error_file_raises():
    """エラーファイルは pd.errors.ParserError になること"""
    csv = make_csv("a,b,c\n1,2\n3,4,5,6") # 列数が行ごとにバラバラ
 
    with pytest.raises(pd.errors.ParserError):
        pd.read_csv(csv)
 
def test_header_only():
    """
    ヘッダーだけ（データ行なし）のCSVは空のDataFrameになること
    エラーではなく「0行のDF」として扱われる。
    """
    csv = make_csv("sales,quantity")
    df = pd.read_csv(csv)
 
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 0
    assert "sales" in df.columns
 
def test_broken_csv():
    """列数が行ごとにバラバラなCSVは ParserError になること"""
    csv = make_csv("a,b,c\n1,2\n3,4,5,6")
 
    with pytest.raises(pd.errors.ParserError):
        pd.read_csv(csv)
 
 
# ================================================================== #
# 実ファイルを使うテスト（tmp_path）
# pytestが自動で用意する一時ディレクトリを使う
# ================================================================== #
def test_reads_csv_file(tmp_path):
    """実際のCSVファイルが読み込めること"""
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("sales,quantity\n1000,10\n2000,20")
 
    df = pd.read_csv(csv_file)
    assert len(df) == 2
 
def test_reads_utf8_bom_csv(tmp_path):
    """
    ExcelがよくBOM付きUTF-8で保存する。
    encoding="utf-8-sig" を指定しないと先頭文字が文字化けする。
    """
    csv_file = tmp_path / "bom.csv"
    csv_file.write_bytes("売上,数量\n1000,10\n".encode("utf-8-sig"))
 
    # BOM付きを正しく読む場合
    df = pd.read_csv(csv_file, encoding="utf-8-sig")
    assert "売上" in df.columns  # BOMが取れていること
