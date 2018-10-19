Deploy the app (Production)
====

# 本番環境構成
* Google App Engine Standard Environment Python3.7
* Google Cloud SQL for PostgreSQL


# 前提条件
* `docs/development/environment.md` で 開発環境構築手順 が完了していること
* python 2.7: Google Cloud SDK の動作に必要


# Google Cloud SDK

## インストール (初回のみ)
Google Cloud の環境構築・デプロイに必要な Google Cloud SDK をインストールする。
```bash
# Google Cloud SDK のインストール
# インストール先とか聞かれるので、環境にあわせて設定
curl https://dl.google.com/dl/cloudsdk/release/install_google_cloud_sdk.bash | bash

# 動作確認
# gcloud コマンドを実行して、エラーがないことを確認
gcloud --version
gcloud components update
gcloud components list
```

## Google Cloud Project の作成 (管理者のみ)
Production 先の Google Cloud Project を作成する。
既に作成済みなので *実行する必要はない！！*
もし、誤って Google Cloud Project を削除した場合に実行する。


### Google Cloud Project
```bash
# Google Cloud の支払いアカウントIDをセット
GCLOUD_BILLING_ACCOUNT_ID=XXXXXX-XXXXXX-XXXXXX
# ユニークな Google Cloud Project ID をセット
GCLOUD_PROJECT_ID=geodjango-postgis-gae-001

# ログイン
# 自動でブラウザが起動するので、Cloud SDK のリクエストを承認
gcloud auth login

# create - Google Cloud Project
# see: https://cloud.google.com/sdk/gcloud/reference/projects/create
gcloud projects create $GCLOUD_PROJECT_ID \
    --name=$GCLOUD_PROJECT_ID

# enable billing
# see: gcloud beta billing projects link
gcloud beta billing projects link $GCLOUD_PROJECT_ID \
    --billing-account=$GCLOUD_BILLING_ACCOUNT_ID

# プロジェクト ID の設定
# create: Google Cloud Project
gcloud config set project $GCLOUD_PROJECT_ID

# enable Cloud SQL Administration API
gcloud services enable sqladmin.googleapis.com

# 確認
gcloud services list --enabled
```

### Google Cloud SQL for PostgreSQL
```bash
# create
# see: https://cloud.google.com/sdk/gcloud/reference/sql/instances/create
gcloud sql instances create app-main \
    --backup \
    --backup-start-time=01:00 \
    --database-flags autovacuum=on \
    --database-version=POSTGRES_9_6 \
    --gce-zone=asia-northeast1-a \
    --maintenance-release-channel=production \
    --maintenance-window-day=TUE \
    --maintenance-window-hour=16 \
    --storage-size=10GB \
    --storage-type=SSD \
    --tier=db-f1-micro

# set postgres user password
# ※ [xxxxxx] を任意の値に置き換え
gcloud sql users set-password postgres no-host \
    --instance=app-main \
    --password=[xxxxxx]

# create database
# see: https://cloud.google.com/sdk/gcloud/reference/sql/databases/create
gcloud sql databases create app-production \
    --instance=app-main

# create user
# ※ [APP_DATABASE_PASSWORD] を任意の値に置き換え
gcloud sql users create app no-host \
    --instance=app-main \
    --password=[APP_DATABASE_PASSWORD]
```

### Google App Engine Standard Environment
```bash
# create
# see: https://cloud.google.com/sdk/gcloud/reference/app/create
gcloud app create \
    --region=asia-northeast1

# アプリから使用する Google Cloud SQL 接続文字列を確認。
# In app.yaml, replace <your-cloudsql-connection-string> with the value of connectionName outputted from the following command:
gcloud beta sql instances describe app-main | grep connectionName

# シークレット情報を RuntimeConfig に設定 (※[APP_DATABASE_PASSWORD]になっている設定値はシステム管理者に確認する)
gcloud services enable runtimeconfig.googleapis.com
gcloud beta runtime-config configs create app-production
gcloud beta runtime-config configs variables set DJANGO_DATABASE_ENGINE django.contrib.gis.db.backends.postgis --config-name app-production
gcloud beta runtime-config configs variables set DJANGO_DATABASE_USER app --config-name app-production
gcloud beta runtime-config configs variables set DJANGO_DATABASE_PASSWORD [APP_DATABASE_PASSWORD] --config-name app-production
gcloud beta runtime-config configs variables set DJANGO_DATABASE_HOST /cloudsql/$GCLOUD_PROJECT_ID:asia-northeast1:app-main --config-name app-production
gcloud beta runtime-config configs variables set DJANGO_DATABASE_PORT 5432 --config-name app-production
gcloud beta runtime-config configs variables set DJANGO_DATABASE_NAME app-production --config-name app-production

# すべての静的コンテンツを 1 つのフォルダにまとめる
pushd app
pyenv activate geodjango-postgis-gae
python manage.py collectstatic --no-input
pyenv deactivate
popd

# ソースをデプロイ
gcloud app deploy app.standard.yaml
```


# 初期設定 (初回デプロイ時のみ)

## パスワード変更

1. Admin サイトにログインする。
   https://geodjango-postgis-gae-001.appspot.com/admin/
    * ログインユーザー: admin
    * パスワード: default
1. パスワードの変更 ページからパスワードを変更する。
   https://geodjango-postgis-gae-001.appspot.com/admin/password_change/
