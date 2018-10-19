Deploy the app (Production)
====

# デプロイ
```bash
git checkout master
git push
```

```bash
# install.md で指定した Google Cloud Project ID をセット
GCLOUD_PROJECT_ID=geodjango-postgis-gae-001

# プロジェクト ID の設定
gcloud config set project $GCLOUD_PROJECT_ID

# すべての静的コンテンツを 1 つのフォルダにまとめる
pushd app
pyenv activate geodjango-postgis-gae
python manage.py collectstatic --no-input
pyenv deactivate
popd

# static files を Cloud Storage バケットにデプロイ
gsutil rsync -R static/ gs://$GCLOUD_PROJECT_ID-static/

# ソースをデプロイ
gcloud app deploy app.flexible.yaml --quiet
```

## 動作確認
```bash
# webブラウザで swagger api explorer が表示されること。
gcloud app browse
```
