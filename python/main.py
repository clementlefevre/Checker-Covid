import logging
import time
import schedule
from services import update_covid


logging.basicConfig(
    filename="covid.log",
    level=logging.DEBUG,
    format="%(asctime)s:%(levelname)s:%(message)s",
)


def job():

    logging.info("Job starts...")
    try:
        update_covid.update_all()
        logging.info("Job finished")
    except Exception as e:
        logging.error("Something went wrong...")
        logging.error(e)


schedule.every().hour.do(job)

time.sleep(60 * 5)

job()

while 1:
    schedule.run_pending()
    time.sleep(1)
