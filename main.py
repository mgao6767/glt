import os
import subprocess
import logging
import logging.config
import logging.handlers
import multiprocessing
import pandas as pd
from datetime import date
from concurrent.futures import ProcessPoolExecutor, as_completed

today = date.today().strftime("%Y-%m-%d")
output_dir = os.path.join("data", today)
log_path = os.path.join("log", f"{today}.log")

if not os.path.exists(output_dir):
    os.makedirs(output_dir)
if not os.path.exists("log"):
    os.makedirs("log")


def worker_init(q):
    # all records from worker processes go to qh and then into q
    qh = logging.handlers.QueueHandler(q)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(qh)


def logger_init():
    q = multiprocessing.Manager().Queue(-1)
    # this is the handler for all log records
    handler = logging.FileHandler(log_path, mode="w")
    handler.setFormatter(
        logging.Formatter("%(levelname)-10s: %(asctime)s - %(name)s - %(message)s")
    )

    # ql gets records from the queue and sends them to the handler
    ql = logging.handlers.QueueListener(q, handler)
    ql.start()

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    # add the handler to the logger so records from this process are handled
    logger.addHandler(handler)

    return ql, q


def glt(gvkey, url, output_dir):
    output_file = f"{gvkey}.html"
    url = "https://" + url
    if os.path.exists(os.path.join(output_dir, output_file)):
        logging.warning(f"{gvkey} {url} already checked. skipped.")
        return
    logging.info(f"{gvkey} {url} check in progress.")
    try:
        subprocess.check_output(
            [
                "lighthouse-ci.cmd",
                url,
                f"--report={output_dir}",
                "--json",
                f"--filename={output_file}",
                "--config-path=config.json",
            ]
        )
        logging.info(f"{gvkey} {url} check completed.")
    except subprocess.CalledProcessError as e:
        logging.error(f"{gvkey} {url} check faliled. {e}")


if __name__ == "__main__":

    df = pd.read_csv("./urls.csv", parse_dates=["deletionDate"])
    df = df[df.weburl.notnull()]

    q_listener, q = logger_init()

    res = []
    logging.info("Start collection.")
    with ProcessPoolExecutor(
        max_workers=10, initializer=worker_init, initargs=(q,)
    ) as exe:
        for row in df.itertuples():
            res.append(exe.submit(glt, row.gvkey, row.weburl, output_dir))

        for _ in as_completed(res):
            pass

    q_listener.stop()
    logging.info("Finished collection.")
