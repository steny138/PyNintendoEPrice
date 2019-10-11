#! /bin/sh

# from script folder move to deploy destination.
cd ../deploy/deploy.ns_web_api.production

# git checkout master branch in heroku repository
# maybe should git pull the newest version from remote repositroy
git checkout master

# move to base folder
cd ../../

# copy deploy need project files
cp -R src/ns_web_crawler/ns_web_crawler/ deploy/deploy.ns_web_crawler.production/ns_web_crawler

# remove the local debug files
rm deploy/deploy.ns_web_crawler.production/ns_web_crawler/.env

# copy git ignore avoid some ignore file been uploading
cp .gitignore deploy/deploy.ns_web_crawler.production

# copy pipfile that install requirement packages
cp -R src/ns_web_crawler/Pipfile deploy/deploy.ns_web_crawler.production/Pipfile
cp -R src/ns_web_crawler/Pipfile.lock deploy/deploy.ns_web_crawler.production/Pipfile.lock

# copy project setting file
cp -R src/ns_web_crawler/scrapy.cfg deploy/deploy.ns_web_crawler.production/scrapy.cfg

# copy procfile from procfiles folder, it decide how to startup the project on heroku
cp deploy/procfiles/ns_web_crawler.production.Procfile deploy/deploy.ns_web_crawler.production/Procfile

# remote to deploy folder
cd deploy/deploy.ns_web_crawler.production

# create a commit prepare pushing to heroku remote repository.
git add -A
git commit -m "production deploy for ns_web_crawler"
git push heroku master -f

# and then, heroku receive the push request, it will start the pipeline flow 
# with build, test, deploy, startup...etc