"""
S3Filesを使う場合のログ書き出しスクリプト

smart_open を使った手法:
  - S3 のパスを通常のファイルと同じ感覚で open() できる
  - ローカルの一時ファイルが不要
  - 書き込み完了と同時に S3 へ反映される

インストール:
  pip install smart_open[s3]
"""

import logging
import smart_open
from datetime import datetime, timezone

# ---- 設定 ----
BUCKET_NAME = "your-log-bucket"
S3_KEY_PREFIX = "app-logs"
# --------------


def get_s3_uri() -> str:
    """書き込み先の S3 URI を生成する。"""
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    return f"s3://{BUCKET_NAME}/{S3_KEY_PREFIX}/{timestamp}.log"


class S3StreamHandler(logging.StreamHandler):
    """smart_open で開いた S3 ファイルオブジェクトへログを書き出すハンドラ。"""

    def __init__(self, s3_uri: str) -> None:
        self._s3_file = smart_open.open(s3_uri, "w", encoding="utf-8")
        try:
            super().__init__(self._s3_file)
        except Exception:
            self._s3_file.close()
            raise

    def close(self) -> None:
        super().close()
        self._s3_file.close()


def setup_logger(s3_uri: str) -> logging.Logger:
    """S3 へ直接書き出すロガーを設定する。"""
    logger = logging.getLogger("app")
    logger.setLevel(logging.DEBUG)

    handler = S3StreamHandler(s3_uri)
    handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logger.addHandler(handler)
    return logger


def main() -> None:
    s3_uri = get_s3_uri()
    print(f"Logging to: {s3_uri}")

    # 1. ロガーをセットアップ（この時点で S3 への書き込みストリームが開く）
    logger = setup_logger(s3_uri)

    # 2. ログを書き出す（ローカルファイルは一切不要）
    logger.info("アプリケーション起動")
    logger.warning("これは警告ログです")
    logger.error("これはエラーログです")
    logger.info("アプリケーション終了")

    # 3. ハンドラを閉じると S3 への書き込みが完了する
    for handler in logger.handlers:
        handler.close()

    print(f"Logged directly to: {s3_uri}")


if __name__ == "__main__":
    main()
