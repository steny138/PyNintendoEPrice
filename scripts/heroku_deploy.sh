#! /bin/sh

git checkout master

cd ../
cp -R src/ns_web_api/web/ deploy/deploy.ns_web_api.stage
cp -R src/ns_web_api/web/ deploy/deploy.ns_web_api.stage
cp .gitignore deploy/deploy.ns_web_api.stage
cp -R src/ns_web_api/Pipfile deploy/deploy.ns_web_api.stage/Pipfile
cp -R src/ns_web_api/Pipfile.lock deploy/deploy.ns_web_api.stage/Pipfile.lock
cp deploy/procfiles/ns_webapi.Production.Procfile deploy/deploy.ns_web_api.stage/Procfile
cd deploy/deploy.ns_web_api.stage
git add -A
git commit -m "production deploy for ns_web_api"
git push heroku master -f
