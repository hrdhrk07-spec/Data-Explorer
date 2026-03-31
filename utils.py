# 汎用的な関数
import logging
import streamlit as st

# ログ設定
logger = logging.getLogger(__name__)

def handle_error(message: str, error: Exception, log: bool = True) -> None:
    """エラーメッセージを表示し、処理を停止するための関数"""
    if log:
        logger.error(f"{message}: {error}")
    st.error(message)
    st.stop()

def raise_error(
        log_level: int, 
        message: str, 
        error: Exception | None, 
        raise_as: type[Exception]
        ) -> None:
    """例外を発生させるための関数"""
    logger.log(log_level, f"{message}: {error}")
    raise raise_as(f"{message}: {error}")