import streamlit as st
import pandas as pd
import plotly.express as px
from typing import Literal, get_args
from streamlit.runtime.uploaded_file_manager import UploadedFile
from ai_summary import summarize_dataframe

# --- 変数 ---
ChartType = Literal["散布図", "棒グラフ", "折れ線グラフ"]

# --- 関数 ---
def load_data(file: UploadedFile) -> pd.DataFrame:
    """CSVを読み込み、基本的なデータクレンジングを行う"""
    try:
        return pd.read_csv(file)
    except pd.errors.ParserError as e:
        st.error(f"CSVの読み込みに失敗しました: {e}")
        st.stop()

def show_summary_stats(df: pd.DataFrame) -> None:
    """統計情報を表示する（戻り値なし）"""
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("基本統計量")
        st.write(df.describe())
    with col2:
        st.subheader("欠損値の確認")
        st.write(df.isnull().sum())

def show_ai_summary(df: pd.DataFrame) -> None:
    """AIによる要約を表示する（戻り値なし）"""
    if st.button("AIによる自動要約を生成"):
        with st.spinner("AIがデータを分析中..."):
            summary = summarize_dataframe(df)
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
    st.set_page_config(page_title="Smart Data Explorer", layout="wide")
    st.title("📊 Smart Data Explorer")

    uploaded_file: UploadedFile | None = st.file_uploader(
        "CSVファイルを選択してください", type="csv"
    )

    if uploaded_file is not None:
        df: pd.DataFrame = load_data(uploaded_file)
        
        tab1, tab2 = st.tabs(["📋 データ概要", "📈 可視化分析"])

        with tab1:
            st.subheader("データプレビュー")
            st.dataframe(df.head())
            show_summary_stats(df)
            show_ai_summary(df)

        with tab2:
            st.subheader("インタラクティブ・チャート")
            cols: list[str] = df.columns.tolist()
            x_axis: str = st.selectbox("X軸を選択", cols)
            y_axis: str = st.selectbox("Y軸を選択", cols)
            c_type: ChartType = st.radio("グラフの種類", get_args(ChartType))
            
            create_plot(df, x_axis, y_axis, c_type)

if __name__ == "__main__":
    main()