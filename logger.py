import logging

def setup_logger():
    logging.basicConfig(
        filename="log.txt",
        level=logging.DEBUG,
        encoding="utf-8",
        format="%(asctime)s [%(levelname)s] %(message)s"
    )
    return logging.getLogger(__name__)