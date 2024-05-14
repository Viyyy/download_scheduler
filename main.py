import requests
import datetime
import os
import dotenv
from urllib.parse import quote
from logger_ import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler

logger = logging.getLogger(__name__)
logger.setLevel('INFO')

dotenv.load_dotenv()
TOWNS = os.getenv('SCHEDULER_TOWNS').split(',')
SAVE_PATH = os.getenv('SCHEDULER_SAVE_PATH')
# SAVE_PATH = os.getcwd()

base_url = 'http://10.166.168.101:8009'

def login():
    logger.info('Login to get access token.')
    url = f'{base_url}/login'

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = {
        'grant_type': '',
        'username': os.getenv('SCHEDULER_USERNAME'),
        'password': os.getenv('SCHEDULER_PASSWORD'),
        'scope': '',
        'client_id': '',
        'client_secret': '',
    }

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        result = response.json()
        return result['access_token']
    else:
        logger.error(f'Failed to login. {response.status_code} {response.text}')

def download_file(api_key:str, town:str, start_date:str, save_path:str=SAVE_PATH):
    logger.info(f'Downloading {town} {start_date}.')
    url = f'{base_url}/census/download/statistics?regions_={quote(town)}&start_date_str={start_date}'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'accept': 'application/json'
    }
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        file_name = f'{town}_{start_date}_{datetime.date.today().strftime("%Y-%m-%d")}.xlsx'
        with open(os.path.join(save_path, file_name), 'wb') as f:
            f.write(res.content)
        logger.info(f'Downloaded {file_name} successfully.')
    else:
        logger.error(f'Failed to download {town} {start_date}. {res.status_code} {res.text}')
        
      
scheduler = AsyncIOScheduler() # 实例化调度器


# @scheduler.scheduled_job('interval', minutes=60) # 每60分钟更新一次当天的数据

# 每天8点执行一次
# @scheduler.scheduled_job('cron', hour=17, minute=30)
@scheduler.scheduled_job('logging', minutes=30)
def download_today_data():
    logger.info('Start downloading today data.')
    api_key = login()
    st = datetime.date.today() - datetime.timedelta(days=os.get('DAYS_BEFORE')).strftime('%Y-%m-%d')
    save_path = os.path.join(SAVE_PATH, datetime.date.today().strftime('%Y-%m-%d'))
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    for t in TOWNS:
        download_file(api_key, t, st, save_path)
    logger.info('End downloading today data.')
              
def main():
    logger.info('Scheduler Start')
    scheduler.start()
    

if __name__ == '__main__':
    main()
    print('ok')