#! /bin/sh

git checkout master

cd ../
cp -R src/ns_web_crawler/ns_web_crawler/ deploy/deploy.ns_web_crawler.production/ns_web_crawler
rm deploy/deploy.ns_web_crawler.production/ns_web_crawler/.env
cp .gitignore deploy/deploy.ns_web_crawler.production
cp -R src/ns_web_crawler/Pipfile deploy/deploy.ns_web_crawler.production/Pipfile
cp -R src/ns_web_crawler/Pipfile.lock deploy/deploy.ns_web_crawler.production/Pipfile.lock
cp -R src/ns_web_crawler/scrapy.cfg deploy/deploy.ns_web_crawler.production/scrapy.cfg
cp deploy/procfiles/ns_web_crawler.production.Procfile deploy/deploy.ns_web_crawler.production/Procfile
cd deploy/deploy.ns_web_crawler.production
git add -A
git commit -m "production deploy for ns_web_crawler"
git push heroku master -f