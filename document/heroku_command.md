
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

# install heroku buildpacks with poetry
```
heroku buildpacks:clear -a ns-eshop-lyc
heroku buildpacks:add https://github.com/moneymeets/python-poetry-buildpack.git -a ns-eshop-lyc
heroku buildpacks:add heroku/python -a ns-eshop-lyc
```