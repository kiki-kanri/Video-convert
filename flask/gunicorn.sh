#!/bin/bash
. ./env.sh

if [ ! -z $1 ] && [ $1 = "--dev" ]; then
	gunicorn -b $host:$port --reload -t 3000 -w 1 main.wsgi #--access-logfile '-' --error-logfile '-'
else
	gunicorn -b $host:$port -k "egg:meinheld#gunicorn_worker" -t 3000 -w $workers main.wsgi
fi
