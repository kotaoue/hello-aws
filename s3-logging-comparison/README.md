# S3 へのログ書き出し: S3Files使用前後の比較

## 疑問

サーバーサイドで動作しているプログラムがログを S3 へ書き出す場合、
S3Files（`smart_open` 等のファイルライクなS3インタフェース）を使うと
どれくらい実装が楽になるのか。

## 比較

### S3Files を使わない場合 ([without_s3files.py](./without_s3files.py))

従来の手法は以下のステップが必要になる。

```
[アプリ] → ローカル一時ファイルに書き込む → boto3 でS3へアップロード → 一時ファイルを削除
```

```python
# 1. 一時ファイルを作成
tmp_file = tempfile.NamedTemporaryFile(...)

# 2. ロガーをセットアップしてログを書き出す
logger = setup_logger(tmp_file.name)
logger.info("アプリケーション起動")
...

# 3. S3 へアップロード
s3.upload_file(tmp_file.name, BUCKET_NAME, s3_key)

# 4. 一時ファイルを削除
os.remove(tmp_file.name)
```

**課題:**

- ローカルにファイルを保持するためディスク容量が必要
- アップロード前にサーバが落ちるとログが失われるリスクがある
- アップロード処理とクリーンアップ処理を自前で実装する必要がある

### S3Files を使う場合 ([with_s3files.py](./with_s3files.py))

`smart_open` を使うと S3 のパスを通常のファイルと同様に扱える。

```
[アプリ] → S3 へ直接書き込む
```

```python
# 1. S3 URIを指定してロガーをセットアップ（一時ファイル不要）
logger = setup_logger("s3://your-bucket/app-logs/20240101_120000.log")
logger.info("アプリケーション起動")
...

# 2. ハンドラを閉じると S3 への書き込みが完了（アップロード処理は不要）
for handler in logger.handlers:
    handler.close()
```

**メリット:**

- ローカルの一時ファイルが不要（ディスク容量を消費しない）
- アップロード処理・クリーンアップ処理の実装が不要
- `open()` と同じ感覚で使えるため、コードがシンプルになる

## 方法

- 環境
  - Python 3.x
  - `boto3` および `smart_open[s3]` がインストールされていること
  - AWS 認証情報が設定されていること（`~/.aws/credentials` または 環境変数）
- 事前準備

  ```bash
  pip install boto3 "smart_open[s3]"
  ```

- 実行方法

  `BUCKET_NAME` 環境変数に自分の S3 バケット名を設定してから実行する。

  ```bash
  export BUCKET_NAME=your-log-bucket

  # S3Files を使わない場合
  python without_s3files.py

  # S3Files を使う場合
  python with_s3files.py
  ```

## 結果

| 観点 | S3Files なし | S3Files あり |
|---|---|---|
| ローカルディスク使用 | 必要 | 不要 |
| アップロード処理の実装 | 必要 | 不要 |
| クリーンアップ処理の実装 | 必要 | 不要 |
| コード量 | 多い | 少ない |
| サーバ停止時のログ消失リスク | あり | 低い（書き込みと同時にS3へ反映） |

## まとめ

`smart_open` のようなファイルライクなS3インタフェースを使うことで、
ロガーの設定先を変えるだけで S3 へ直接書き出せるようになる。
一時ファイルの作成・削除やアップロード処理が不要になるため、
コードがシンプルになり、ディスク容量やログ消失のリスクも軽減できる。

## 参考資料

- [smart\_open – GitHub](https://github.com/piskvorky/smart_open)
- [Amazon S3 へのオブジェクトのアップロード – AWS ドキュメント](https://docs.aws.amazon.com/ja_jp/AmazonS3/latest/userguide/upload-objects.html)
- [boto3 S3 ドキュメント](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html)
