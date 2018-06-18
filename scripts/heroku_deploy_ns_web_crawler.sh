#! /bin/sh

git checkout master

cd ../
cp -R src/ns_web_crawler/ns_web_crawler/ deploy/deploy.deploy.ns_web_crawler.production
cp .gitignore deploy/deploy.deploy.ns_web_crawler.production
cp -R src/ns_web_crawler/Pipfile deploy/deploy.ns_web_crawler.production/Pipfile
cp -R src/ns_web_crawler/Pipfile.lock deploy/deploy.ns_web_crawler.production/Pipfile.lock
cp deploy/procfiles/ns_web_crawler.production deploy/deploy.ns_web_crawler.production/Procfile
cd deploy/deploy.deploy.ns_web_crawler.production
git add -A
git commit -m "production deploy for ns_web_crawler"
git push heroku master -f