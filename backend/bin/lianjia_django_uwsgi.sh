#!/usr/bin/env bash


PROJECT_PATH=/home/.jywcode/lianjia/backend
DESC=lianjia_django_server
NAME=lianjia_django_server
PIDFILE=$PROJECT_PATH/uwsgi/uwsgi.pid
STATUS_FILE=$PROJECT_PATH/uwsgi/uwsgi.status
DAEMONIZE_FILE=$PROJECT_PATH/uwsgi/$NAME.log

server_start() {
     source /home/.jywcode/lianjia/backend/venv/bin/activate
     uwsgi --ini $PROJECT_PATH/uwsgi/lianjia.ini --stats=$STATUS_FILE --pidfile=$PIDFILE --daemonize=$DAEMONIZE_FILE
}


server_stop() {
    source /home/.jywcode/lianjia/backend/venv/bin/activate
    uwsgi --stop $PIDFILE
}

server_status() {
#    start-stop-daemon --status --quiet --pidfile $PIDFILE
    source /home/.jywcode/lianjia/backend/venv/bin/activate
    uwsgi --connect-and-read $STATUS_FILE
    return $?
}


case "$1" in
        start)
            echo -n "Starting $DESC: "
        if [ -e $PIDFILE ]
        then
           echo "The program has been started! Please check it!"
        else
            server_start
            sleep 5
                if [ -e $PIDFILE ]
            then
                        echo "Ok"
            else
            echo "Failed"
            fi
        fi
                ;;
        stop)
                echo -n "Stopping $DESC: "
        if [ ! -e $PIDFILE ]
                then
                   echo "The program doesn't start!"
                else
                    server_stop
            sleep 5
            if [ ! -e $PIDFILE ]
            then
                        echo "ok"
            fi
        fi
                ;;
        restart|force-reload)
                echo -n "Restarting $DESC: "
                server_stop
        sleep 5
        if [ -e $PIDFILE ]
        then
            echo "stop failed!"

        else
            echo "stop ok!"
        fi

                server_start
        sleep 5
        if [ -e $PIDFILE ]
                then
                    echo "start ok!"

                else
                    echo "start Failed!"
                fi
                ;;
        status)
                echo -n "Status of $DESC: "
                server_status && echo "running" || echo "stopped"
                ;;
        *)
                N=/etc/init.d/$NAME
                echo "Usage: $N {start|stop|restart|status}" >&2
                exit 1
                ;;
esac

exit 0
