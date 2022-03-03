#! /bin/sh

cd ../deploy/deploy.ns_web_api.production
git checkout master

cd ../../
cp -R src/ns_web_api/ns_web_api/ deploy/deploy.ns_web_api.production/ns_web_api
cp .gitignore deploy/deploy.ns_web_api.production
cp -R src/ns_web_api/pyproject.toml deploy/deploy.ns_web_api.production/pyproject.toml
cp -R src/ns_web_api/poetry.lock deploy/deploy.ns_web_api.production/poetry.lock
cp deploy/procfiles/ns_webapi.production.Procfile deploy/deploy.ns_web_api.production/Procfile
cd deploy/deploy.ns_web_api.production
git add -A
git commit -m "production deploy for ns_web_api"
git push heroku master -f
