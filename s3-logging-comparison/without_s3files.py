"""
S3Filesを使わない場合のログ書き出しスクリプト

従来の手法:
  1. ローカルの一時ファイルにログを書き出す
  2. boto3 を使ってそのファイルを S3 へアップロードする
  3. 一時ファイルを削除する

問題点:
  - ローカルにファイルを保持するためディスク容量が必要
  - アップロード前にサーバが落ちるとログが失われるリスクがある
  - アップロードとクリーンアップの処理を自前で書く必要がある
"""

import boto3
import logging
import os
import tempfile
from datetime import datetime, timezone

# ---- 設定 ----
BUCKET_NAME = "your-log-bucket"
S3_KEY_PREFIX = "app-logs"
# --------------


def get_s3_key() -> str:
    """アップロード先の S3 キーを生成する。"""
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    return f"{S3_KEY_PREFIX}/{timestamp}.log"


def setup_logger(log_path: str) -> logging.Logger:
    """ローカルファイルへ書き出すロガーを設定する。"""
    logger = logging.getLogger("app")
    logger.setLevel(logging.DEBUG)

    handler = logging.FileHandler(log_path, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logger.addHandler(handler)
    return logger


def upload_to_s3(local_path: str, bucket: str, key: str) -> None:
    """ローカルファイルを S3 へアップロードする。"""
    s3 = boto3.client("s3")
    s3.upload_file(local_path, bucket, key)
    print(f"Uploaded: s3://{bucket}/{key}")


def main() -> None:
    # 1. ローカルの一時ファイルを作成
    tmp_file = tempfile.NamedTemporaryFile(
        mode="w", suffix=".log", delete=False, encoding="utf-8"
    )
    log_path = tmp_file.name
    tmp_file.close()

    try:
        # 2. ロガーをセットアップしてログを書き出す
        logger = setup_logger(log_path)

        logger.info("アプリケーション起動")
        logger.warning("これは警告ログです")
        logger.error("これはエラーログです")
        logger.info("アプリケーション終了")

        # ロガーのハンドラを閉じてファイルをフラッシュ
        for handler in logger.handlers:
            handler.close()

        # 3. S3 へアップロード
        s3_key = get_s3_key()
        upload_to_s3(log_path, BUCKET_NAME, s3_key)

    finally:
        # 4. 一時ファイルを削除
        if os.path.exists(log_path):
            os.remove(log_path)
            print(f"Removed temporary file: {log_path}")


if __name__ == "__main__":
    main()
