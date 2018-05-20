#! /bin/sh

cd ../
cp -R src/ns_web_api/web deploy/deploy.ns_web_api.stage
cp .gitignore deploy/deploy.ns_web_api.stage
cp deploy/procfiles/media.procfile deploy/deploy.ns_web_api.stage/Procfile
cd deploy/deploy/deploy.ns_web_api.stage
git add -A
git commit -m "production deploy for ns_web_api"
git push heroku master -f
