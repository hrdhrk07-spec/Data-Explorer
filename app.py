import streamlit as st
import pandas as pd
import plotly.express as px
from typing import List

# --- 内部ロジックの関数 ---

def load_data(file: st.runtime.uploaded_file_manager.UploadedFile) -> pd.DataFrame:
    """CSVを読み込み、基本的なデータクレンジングを行う"""
    df: pd.DataFrame = pd.read_csv(file)
    return df

def show_summary_stats(df: pd.DataFrame) -> None:
    """統計情報を表示する（戻り値なし）"""
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("基本統計量")
        st.write(df.describe())
    with col2:
        st.subheader("欠損値の確認")
        st.write(df.isnull().sum())

def create_plot(df: pd.DataFrame, x: str, y: str, chart_type: str) -> None:
    """選択された設定でグラフを作成して表示する"""
    if chart_type == "散布図":
        fig = px.scatter(df, x=x, y=y)
    elif chart_type == "棒グラフ":
        fig = px.bar(df, x=x, y=y)
    else:
        fig = px.line(df, x=x, y=y)
    
    fig.update_layout(autosize=True)
    st.plotly_chart(fig, width="stretch")

# --- メイン処理 ---

def main() -> None:
    st.set_page_config(page_title="Smart Data Explorer", layout="wide")
    st.title("📊 Smart Data Explorer")

    uploaded_file: st.runtime.uploaded_file_manager.UploadedFile | None = st.file_uploader(
        "CSVファイルを選択してください", type="csv"
    )

    if uploaded_file is not None:
        df: pd.DataFrame = load_data(uploaded_file)
        
        tab1, tab2 = st.tabs(["📋 データ概要", "📈 可視化分析"])

        with tab1:
            st.subheader("データプレビュー")
            st.dataframe(df.head())
            show_summary_stats(df)

        with tab2:
            st.subheader("インタラクティブ・チャート")
            cols: List[str] = df.columns.tolist()
            x_axis: str = st.selectbox("X軸を選択", cols)
            y_axis: str = st.selectbox("Y軸を選択", cols)
            c_type: str = st.radio("グラフの種類", ["散布図", "棒グラフ", "折れ線グラフ"])
            
            create_plot(df, x_axis, y_axis, c_type)

if __name__ == "__main__":
    main()