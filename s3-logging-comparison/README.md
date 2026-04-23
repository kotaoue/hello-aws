# S3 へのログ書き出し: S3Files使用前後の比較

## スクリプトの実行方法

### 事前準備

```bash
pip install boto3 "smart_open[s3]"
```

### 実行

```bash
export BUCKET_NAME=your-log-bucket

# S3Files を使わない場合
python without_s3files.py

# S3Files を使う場合
python with_s3files.py
```

## 比較

| | S3Files なし ([without_s3files.py](./without_s3files.py)) | S3Files あり ([with_s3files.py](./with_s3files.py)) |
|---|---|---|
| 一時ファイル | 必要 | 不要 |
| アップロード処理 | 自前で実装 | 不要 |
| クリーンアップ処理 | 自前で実装 | 不要 |

## 参考資料

- [smart\_open – GitHub](https://github.com/piskvorky/smart_open)
- [Amazon S3 へのオブジェクトのアップロード – AWS ドキュメント](https://docs.aws.amazon.com/ja_jp/AmazonS3/latest/userguide/upload-objects.html)
- [boto3 S3 ドキュメント](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html)
