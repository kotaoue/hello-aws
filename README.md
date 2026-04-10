# hello-aws

I want to resolve my AWS questions.

---

## ローカルで AWS CLI を使えるようにする手順

### 前提条件

- AWS アカウントを持っていること
- IAM ユーザーの **アクセスキー ID** と **シークレットアクセスキー** を発行済みであること

### 1. AWS CLI のインストール

**macOS (Homebrew)**
```bash
brew install awscli
```

**Linux**
```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

**Windows**
```powershell
msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi
```

インストールの確認:
```bash
aws --version
```

### 2. クレデンシャルの設定

```bash
aws configure
```

対話形式で以下の情報を入力します:

```
AWS Access Key ID [None]: <アクセスキー ID>
AWS Secret Access Key [None]: <シークレットアクセスキー>
Default region name [None]: ap-northeast-1
Default output format [None]: json
```

入力した情報は以下のファイルに保存されます:

| ファイル | 内容 |
|---|---|
| `~/.aws/credentials` | アクセスキー ID・シークレットアクセスキー |
| `~/.aws/config` | リージョン・出力形式 |

### 3. 動作確認

設定が正しいかどうかを確認するには、以下のコマンドを実行します:

```bash
# 認証情報の確認
aws sts get-caller-identity

# S3 バケット一覧の取得
aws s3 ls

# EC2 インスタンス一覧の取得
aws ec2 describe-instances --query 'Reservations[*].Instances[*].[InstanceId,State.Name]' --output table
```

### 4. 複数プロファイルの管理（オプション）

複数の AWS アカウントや IAM ユーザーを使い分けたい場合は、`--profile` オプションを活用します。

```bash
# 新しいプロファイルを追加する
aws configure --profile <プロファイル名>

# プロファイルを指定してコマンドを実行する
aws s3 ls --profile <プロファイル名>

# 環境変数でデフォルトプロファイルを指定する
export AWS_PROFILE=<プロファイル名>
aws s3 ls
```

### 参考資料

- [AWS CLI のインストールと設定 (公式)](https://docs.aws.amazon.com/ja_jp/cli/latest/userguide/getting-started-install.html)
- [AWS CLI の設定ファイルと認証情報ファイルの設定 (公式)](https://docs.aws.amazon.com/ja_jp/cli/latest/userguide/cli-configure-files.html)
