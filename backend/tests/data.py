import os

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.backend.settings')
django.setup()
from backend.crawl.ershoufang_crawler import ErShouFangCrawler

ershoufang = ErShouFangCrawler()
