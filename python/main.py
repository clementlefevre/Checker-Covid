import logging

import time
import schedule
from services import update_covid


logging.basicConfig(
    filename="covid.log",
    level=logging.DEBUG,
    format="%(asctime)s:%(levelname)s:%(message)s",
)

logging.getLogger("requests.packages.urllib3.connectionpool").setLevel(logging.ERROR)


def job():

    logging.info("Job starts...")
    try:
        update_covid.update_all()
        logging.info("Job finished")
    except Exception as e:
        logging.error("Something went wrong during the job execution :")
        logging.exception(e)
        logging.critical(e, exc_info=True)


schedule.every().hour.do(job)

time.sleep(60 * 5)

job()

while 1:
    schedule.run_pending()
    time.sleep(1)
