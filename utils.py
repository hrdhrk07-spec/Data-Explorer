# 汎用的な関数
import logging
import streamlit as st

# ログ設定
logger = logging.getLogger(__name__)

def handle_error(user_message: str, ex_message: str, log: bool = True) -> None:
    """ログ記録後にエラーメッセージを表示し、処理を停止するための関数"""
    if log:
        logger.error(f"{user_message}: {ex_message}")
    st.error(user_message)
    st.stop()

def raise_error(
        log_level: int, 
        message: str, 
        error: Exception | None, 
        raise_as: type[Exception]
        ) -> None:
    """ログ記録後に例外を発生させるための関数"""
    logger.log(log_level, f"{message}: {str(error)}" if error else message)
    raise raise_as(f"{message}: {str(error)}" if error else message)