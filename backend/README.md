# 链家房产数据爬取分析可视化平台后端
```bash
创建环境

cd backend
virtualenv venv
source bin/activate

安装依赖

pip install -r requirements.txt

运行

python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0:8000

开启 celery 队列

celery -A backend.celery worker -l info

```