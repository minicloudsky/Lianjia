#! /usr/bin/python

/home/lck/software/pyenv/versions/3.6.6/bin/gunicorn -w 2 --forwarded-allow-ips=* --bind=0.0.0.0:1126 noah_opendata.wsgi:application --chdir /home/lck/winshared/apps/devops/noah_opendata/ --access-logfile /tmp/apollo-backend-access.log --error-logfile /tmp/apollo-backend-error.log 
