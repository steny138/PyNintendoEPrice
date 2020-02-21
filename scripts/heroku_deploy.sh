#! /bin/sh

cd ../deploy/deploy.ns_web_api.production
git checkout master

cd ../../
cp -R src/ns_web_api/web/ deploy/deploy.ns_web_api.production
cp -R src/ns_web_api/web/ deploy/deploy.ns_web_api.production
cp .gitignore deploy/deploy.ns_web_api.production
cp -R src/ns_web_api/Pipfile deploy/deploy.ns_web_api.production/Pipfile
cp -R src/ns_web_api/Pipfile.lock deploy/deploy.ns_web_api.production/Pipfile.lock
cp deploy/procfiles/ns_webapi.production.Procfile deploy/deploy.ns_web_api.production/Procfile
cd deploy/deploy.ns_web_api.production
git add -A
git commit -m "production deploy for ns_web_api"
git push heroku master -f
