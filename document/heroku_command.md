
# link to hroku db with heroku cli by psql.

```
heroku pg:psql -a [heroku app name]
```

# Deploy to heroku with git push to heroku
## it will auto make a new commit like a version, and push to heroku repository, and then it will trigger the heroku deploy flow.

```
cd scripts
sh heroku_deploy.sh
```