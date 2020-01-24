import random

useragents = [
    'Mozilla/5.0 (iPhone; CPU iPhone OS 9_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13C75 Safari/601.1',
    'Mozilla/5.0 (iPad; CPU OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53',
    'Mozilla/5.0 (Android 4.4; Mobile; rv:41.0) Gecko/41.0 Firefox/41.0',
]
cookies = [
    'select_city=110000; lianjia_uuid=9beb0cfd-b533-4234-8984-94160c92048d; TY_SESSION_ID=a30a8787-384d-4cca-940b-9d2364079106; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216fd11d35e3526-0311dc74442ecc-c383f64-1049088-16fd11d35e445e%22%2C%22%24device_id%22%3A%2216fd11d35e3526-0311dc74442ecc-c383f64-1049088-16fd11d35e445e%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; UM_distinctid=16fd11d3d2018b-0f165dde3ce79e-c383f64-100200-16fd11d3d211c8; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1579761352; _ga=GA1.2.811292479.1579761352; _gid=GA1.2.705651448.1579761352; lianjia_ssid=a2046229-e31c-d4cd-9c3c-16baf3a386bb; CNZZDATA1254525948=593127208-1579758445-%7C1579826545; CNZZDATA1253491255=1976497044-1579759938-%7C1579828938; _gat=1; _gat_past=1; _gat_new=1; _gat_global=1; _gat_new_global=1; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiMGEzOWJlMDQ2MTYxY2VmNDcxYzkwNWNlM2E0Yjk4ZTlmZDdhNWM3NGZkNTcwOWQxYmZiNWZhYzE0YTYwNzFhYTYwMDRlMjYzYWQ0MGUxNDdmNmY1YmEwZDIyMWM1NGJiZWI1MGNmMWJhZTlmMGE5YmZhNDIwZjYzN2RlMGNlNzkyYjFhOThlZjY4ZjYxZWYzOTkxNThhM2VkODEzNmYxNTAzZmE0ZmY4N2Y4NjEyOTQwNzZiNWZjMzY4Y2U4YTY0MDcwMjk3NjMxMmI2ODliNjlkYWE0YjZlZTAzNTdhMTM1ZWY2Y2ZjNTc1ZmNmMzVlZDE3MGFmYWQ0M2I1ZTNiMzQ3MjFmNGEzMTE3Mzc4MTgzZmY5OWZmZTk2Y2RhNTY1NmIzYzhhMmI5YTMwNWE1NjY1NjUyOTM2MWU0Y2UyZWZcIixcImtleV9pZFwiOlwiMVwiLFwic2lnblwiOlwiNWRlMGU4YWNcIn0iLCJyIjoiaHR0cHM6Ly9tLmxpYW5qaWEuY29tL2NpdHkvIiwib3MiOiJ3ZWIiLCJ2IjoiMC4xIn0=; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1579829773',

]


def header():
    return {
        'User-Agent': random.choice(useragents),
        'Cookie': random.choice(cookies),
        'Referer': 'https://m.lianjia.com/',
    }
