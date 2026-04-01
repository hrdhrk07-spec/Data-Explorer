# app.py のテストコード
# 実行方法:
#    pytest tests/test_app.py -v
 
import io
import pytest
import pandas as pd

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
