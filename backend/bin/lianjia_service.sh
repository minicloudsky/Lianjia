#!/usr/bin/env bash


PROJECT_PATH=/home/.jywcode/lianjia/backend
DESC=lianjia_spider_project


server_start() {
    sh $PROJECT_PATH/bin/lianjia_django_uwsgi.sh start
    sh $PROJECT_PATH/bin/lianjia_celery.sh start
}

server_stop() {
    sh $PROJECT_PATH/bin/lianjia_django_uwsgi.sh stop
    sh $PROJECT_PATH/bin/lianjia_celery.sh stop
}

server_restart() {
    sh $PROJECT_PATH/bin/lianjia_django_uwsgi.sh restart
    sh $PROJECT_PATH/bin/lianjia_celery.sh restart
}


case "$1" in
        start)
            echo -n "Starting $DESC: "
            server_start
                ;;
        stop)
            echo -n "Stopping $DESC: "
            server_stop
                ;;
        restart|force-reload)
            echo -n "Restarting $DESC: "
            server_restart
                ;;

esac

exit 0