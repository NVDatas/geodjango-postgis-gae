開発環境構築手順 on ローカルマシン
=============================

ローカルマシン上に軽量な開発用ウェブサーバを立ち上げて開発環境を構築する手順を記述する。

開発用ウェブサーバは必要に応じて自動的にPythonコードをリロードする。
コードの変更を反映させるためにいちいちサーバを再起動する必要が無いため、迅速な開発が可能。
また、 [PyCharm](https://www.jetbrains.com/pycharm/) Debugger 等を使用して、ステップ実行が可能。

# production 環境との違い
* ほぼ同じ
    * PostgreSQL のメジャーバージョンは同じ。マイナーバージョンは違う可能性あり。


# System Requirements
* Mac OS X 10.12.x (Sierra) or later
* バージョン管理システム: Git (OS付属もしくはHomebrewでインストール)
* [Homebrew 1.2.x](https://github.com/Homebrew/homebrew)
* [Docker for Mac](https://www.docker.com/docker-mac)
    * DB: PostgreSQL 9.6 on Docker


# 開発環境構築手順

## Homebrew
インストール手順は <http://brew.sh/> を参照。

## Docker for Mac
インストール手順は <https://docs.docker.com/docker-for-mac/install/#what-to-know-before-you-install> を参照。


## pyenv + virtualenv
```bash
brew install pyenv pyenv-virtualenv
```

## 環境設定
```bash
cat << 'EOF' | tee -a ~/.bashrc

# homebrew-pyenv
if which pyenv > /dev/null; then
    eval "$(pyenv init -)"
fi
if which pyenv-virtualenv-init > /dev/null; then
    export PYENV_VIRTUALENV_DISABLE_PROMPT=0
    eval "$(pyenv virtualenv-init -)";
fi
EOF
```

反映するため、Terminal を再起動


## ソースのダウンロード
```bash
git clone https://github.com/miyagi389/geodjango-postgis-gae.git
```

## 開発用バックエンドミドルウェアの起動
Docker で PostgreSQL を起動する。
```bash
pushd docker/development

# バックグラウンドで起動
docker-compose up -d
# 正常に起動したか確認
docker-compose ps

popd
```

## python 仮想環境の作成
```bash
# インストール可能なバージョンの一覧を確認
pyenv install -l

# python 3.x のインストール
pyenv install 3.6.6

# python 仮想環境の作成
pyenv virtualenv 3.6.6 geodjango-postgis-gae
```

# 初期設定
```bash
# 初期設定は、pyenv上の環境に対して行う。
pyenv activate geodjango-postgis-gae

# python パッケージのインストール
pip install -r requirements.txt
pip install -r requirements-development.txt

# データベースの作成/移行
pushd app
python manage.py migrate

# 管理者ユーザーアカウントの作成
## username: admin でアカウント作成 & パスワードを設定
python manage.py createsuperuser --username=admin --email=admin@localhost --noinput \
&& python manage.py changepassword admin

# 初期データの投入
python manage.py loaddata 001_geo_japan.json

popd
```

## 実行
```bash
pushd app

# ローカルHTTPサーバを起動する。
python manage.py runserver

popd
```

# 開発開始手順 (2回目以降)

## Docker for Mac の起動
Docker for Mac のデフォルトインストールオプションだと自動起動している。
手動起動している場合は、起動する。

## 開発用バックエンドミドルウェアの起動
```bash
cd docker/development
# バックグラウンドで起動
docker-compose up -d
```

## python 仮想環境に入る
```bash
pyenv activate geodjango-postgis-gae
```

## ローカルHTTPサーバの起動
```bash
cd app
# ローカルHTTPサーバを起動する。
python manage.py runserver
```

## 開発
* ソースコードを編集する。
* http://127.0.0.1:8080/admin/ をWebブラウザで開いて動作確認する。
* http://127.0.0.1:8080/api/docs/swagger/ をWebブラウザで開いて動作確認する。


# 開発終了手順

## ローカルHTTPサーバの停止
ローカルHTTPサーバを起動したTerminalでCtrl+Cキーを入力して停止する。

## python 仮想環境を抜ける
```bash
pyenv deactivate
```

## 開発用バックエンドミドルウェアの停止
```bash
cd docker/development
# 停止
docker-compose stop
```

## Docker for Mac の停止
macOS のメニューから Docker for Mac のアイコンをクリックして表示されるコンテキストメニューから "Quit for Docker" をクリックする。


# アンインストール

## 開発用バックエンドミドルウェアのアンインストール
```bash
cd docker/development
# コンテナとコンテナが作成したデータボリュームを削除
docker-compose rm -v --force
```
