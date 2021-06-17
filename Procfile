heroku buildpacks:set heroku/LANG
heroku buildpacks:add https://github.com/matteotiziano/heroku-buildpack-tesseract
web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker webapp:app