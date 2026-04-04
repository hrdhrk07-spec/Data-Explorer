import streamlit as st
import pandas as pd
import plotly.express as px
import logging
from constants import ErrorMessage, Dropdown_Missing, Dropdown_Outlier, HIGHLIGHT_OUTLIER, HIGHLIGHT_MISSING
from typing import Literal, get_args
from streamlit.runtime.uploaded_file_manager import UploadedFile
from ai_summary import summarize_dataframe
from utils import handle_error

# ログ初期設定（全体で一度だけ呼びだせばよい）
logging.basicConfig(
        filename="log.txt",
        level=logging.DEBUG,
        encoding="utf-8",
        format="%(asctime)s [%(levelname)s] %(message)s"
)

# 変数
ChartType = Literal["散布図", "棒グラフ", "折れ線グラフ"]

# 関数
def load_data(file: UploadedFile) -> pd.DataFrame:
    """CSVを読み込み、基本的なデータクレンジングを行う"""
    try:
        return pd.read_csv(file)
    except pd.errors.EmptyDataError as e:
        handle_error(ErrorMessage.CSV_EMPTY.value, str(e))
    except pd.errors.ParserError as e:
        handle_error(ErrorMessage.CSV_PARSE_ERROR.value, str(e))
    except Exception as e:
        handle_error(ErrorMessage.CSV_LOAD_ERROR.value, str(e))

def show_summary_stats(df: pd.DataFrame) -> None:
    """統計情報を表示する（戻り値なし）"""
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("基本統計量")
        st.write(df.describe())
    with col2:
        st.subheader("欠損値の確認")
        st.write(df.isnull().sum())

def compute_iqr_bounds(series: pd.Series) -> tuple[float, float]:
    """IQR法でlower/upperの境界値を返す。"""
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    return lower, upper

def detect_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """IQR法で数値列の外れ値フラグを返す"""

    # 引数と同じ形のDataFrameを作り、全てのセルをFalseで初期化
    outlier_flags = pd.DataFrame(False, index=df.index, columns=df.columns)
    
    # 引数のDataFrameの数値列のみを取り出し、列名一覧を取得
    numeric_cols = df.select_dtypes(include="number").columns

    for col in numeric_cols:

        # 列ごとにIQRの境界値を計算
        lower, upper = compute_iqr_bounds(df[col])

        # 下限または上限を外れたデータをTrueとするフラグを立てる
        outlier_flags[col] = (df[col] < lower) | (df[col] > upper)

    return outlier_flags

def build_highlight_styles(df: pd.DataFrame, outlier_flags: pd.DataFrame, missing_flags: pd.DataFrame) -> pd.Styler:
    """外れ値セルにCSSスタイルを付与したStylerを返す"""
    def highlight(col: pd.Series) -> list[str]:
        styles = []
        for i in col.index:
            if outlier_flags.loc[i, col.name]:
                styles.append(f"background-color: {HIGHLIGHT_OUTLIER}")
            elif missing_flags.loc[i, col.name]:
                styles.append(f"background-color: {HIGHLIGHT_MISSING}")
            else:
                styles.append("")
        return styles
    # apply()は axis=0 の場合列ごとに関数を呼び出す
    return df.style.apply(highlight, axis=0)

def apply_missing_strategy(df: pd.DataFrame, strategy: str) -> pd.DataFrame:
    """欠損値を指定した方法で処理する。"""
    if strategy == Dropdown_Missing.ROW_DROP.value:
        return df.dropna()
    elif strategy == Dropdown_Missing.MEAN_FILL.value:
        return df.fillna(df.mean(numeric_only=True))
    elif strategy == Dropdown_Missing.ZERO_FILL.value:
        num_cols = df.select_dtypes(include="number").columns
        str_cols = df.select_dtypes(include="object").columns
        df[num_cols] = df[num_cols].fillna(0)
        df[str_cols] = df[str_cols].fillna("Missing")
        return df
    return df  # "処理しない" の場合はそのまま返す

def apply_outlier_strategy(df: pd.DataFrame, strategy: str) -> pd.DataFrame:
    """外れ値を指定した方法で処理する（数値列のみ）。"""
    if strategy == Dropdown_Outlier.ROW_DROP.value:
        # 欠損値を加工している可能性があるため、外れ値フラグを再度取得
        outlier_flags_new = detect_outliers(df)
        # 1行でも外れ値があればTrueとなるマスクを作成
        mask = outlier_flags_new.any(axis=1)
        # 外れ値が無い行を抽出し、インデックスを振り直す
        return df[~mask].reset_index(drop=True) 
    elif strategy == Dropdown_Outlier.IQR_CLIP.value:
        df = df.copy()
        for col in df.select_dtypes(include="number").columns:
            # 列ごとにIQRの境界値を計算
            lower, upper = compute_iqr_bounds(df[col])
            # 下限を下回る値はlowerに、上限を上回る値はupperに置き換える
            df[col] = df[col].clip(lower=lower, upper=upper)
        return df
    return df # "処理しない" の場合はそのまま返す

def convert_df_to_csv(df: pd.DataFrame) -> bytes:
    """DataFrameをCSVのバイト列に変換する。"""
    return df.to_csv(index=False).encode("utf-8-sig")  # Excel対応のBOM付きUTF-8

def show_ai_summary(df: pd.DataFrame) -> None:
    """AIによる要約を表示する（戻り値なし）"""
    if st.button("AIによる自動要約を生成"):
        with st.spinner("AIがデータを分析中..."):
            try:
                summary = summarize_dataframe(df)
            except Exception as e:
                # エラーはai_summary.pyでログに記録済みなので、ユーザーへの通知のみ
                # AI要約の失敗時はユーザにもエラーメッセージを表示し、処理を停止する。
                handle_error(f"{ErrorMessage.AI_SUMMARY_FAILED.value}: {str(e)}", "", log=False)
        st.info(summary)

def create_plot(df: pd.DataFrame, x: str, y: str, chart_type: ChartType) -> None:
    """選択された設定でグラフを作成して表示する"""
    if chart_type == "散布図":
        fig = px.scatter(df, x=x, y=y)
    elif chart_type == "棒グラフ":
        fig = px.bar(df, x=x, y=y)
    else:
        fig = px.line(df, x=x, y=y)
    
    st.plotly_chart(fig, width="stretch")

# --- メイン処理 ---

def main() -> None:
    st.set_page_config(page_title="Data Explorer", layout="wide")
    st.title("📊 Data Explorer")

    uploaded_file: UploadedFile | None = st.file_uploader(
        "CSVファイルを選択してください", type="csv"
    )

    if uploaded_file is not None:
        df: pd.DataFrame = load_data(uploaded_file)       
        tab1, tab2 = st.tabs(["📋 データ概要", "📈 可視化分析"])

        with tab1:
            st.subheader("データプレビュー")
            st.dataframe(df.head())

            # --- 統計情報の表示 ---
            show_summary_stats(df)

            # --- 外れ値・欠損値ハイライト ---
            st.subheader("🔴 外れ値（IQR法）・欠損値ハイライト")

            # 外れ値・欠損値フラグ表の作成と集計
            outlier_flags: pd.DataFrame = detect_outliers(df)
            missing_flags: pd.DataFrame = df.isnull()
            outlier_count: int = outlier_flags.sum().sum()
            missing_count: int = missing_flags.sum().sum()

            if outlier_count == 0 and missing_count == 0:
                st.success("外れ値・欠損値は検出されませんでした。")
            else:
                if outlier_count > 0:
                    st.warning(f"外れ値が {outlier_count} 件検出されました。")
                if missing_count > 0:
                    st.warning(f"欠損値が {missing_count} 件検出されました。")  
                st.dataframe(
                    build_highlight_styles(df, outlier_flags, missing_flags)
                )
            
            col1, col2 = st.columns(2)
            with col1:
                missing_strategy = st.selectbox(
                    "欠損値の処理",
                    [strategy.value for strategy in Dropdown_Missing],
                )
            with col2:
                outlier_strategy = st.selectbox(
                    "外れ値の処理",
                    [strategy.value for strategy in Dropdown_Outlier],
                )

            # --- データ加工 ---
            df_processed = apply_missing_strategy(df, missing_strategy)
            # 外れ値処理は欠損値処理の後に行う。欠損値処理でデータの削除・補完をすることで外れ値の判定が変わる可能性があるため。
            df_processed = apply_outlier_strategy(df_processed, outlier_strategy)

            # --- 加工後の行数表示 ---
            st.caption(f"加工後の行数：{len(df_processed)} 行（元データ：{len(df)} 行）")

            # --- 加工後CSVのダウンロード ---
            csv_bytes = convert_df_to_csv(df_processed)
            st.download_button(
                label="📥 データ加工済みCSVをダウンロード",
                data=csv_bytes,
                file_name="data_processed.csv",
                mime="text/csv",
            )

            # --- AI要約 ---
            show_ai_summary(df)

        with tab2:
            st.subheader("インタラクティブ・チャート")
            cols: list[str] = df.columns.tolist()
            x_axis: str = st.selectbox("X軸を選択", cols)
            y_axis: str = st.selectbox("Y軸を選択", cols)
            c_type: ChartType = st.radio("グラフの種類", get_args(ChartType))
            
            # --- グラフの作成と表示 ---
            create_plot(df, x_axis, y_axis, c_type)

if __name__ == "__main__":
    main()