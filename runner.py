import logging
import random
import time

from config import DELAY_RANGE, MIN_LEN, MAX_LEN
from fetcher import fetch_and_extract
from progress import init_progress, load_progress, save_progress
from retry import load_retry, init_retry, save_retry, delete_retry
from utils import brute_code_at, total_combinations, load_dictionary

logger = logging.getLogger(__name__)


def process_code(code, stage, length=0, index=0, retry=False):
    success, failed_code = fetch_and_extract(code)

    progress = load_progress()
    progress["stage"] = stage
    if stage == "dict":
        progress["dict_index"] = index + 1
    else:
        progress["brute_len"] = length
        progress["brute_index"] = index + 1
    save_progress(progress)

    if (not success or failed_code) and (not retry):
        save_retry(code)
    if (success and not failed_code) and retry:
        logger.info(f"delete retry: {code}")
        delete_retry(code)

    time.sleep(random.uniform(*DELAY_RANGE))


def run():
    init_progress()
    init_retry()

    progress = load_progress()
    dict_index = progress.get("dict_index", 0)
    brute_len = progress.get("brute_len", MIN_LEN)
    brute_index = progress.get("brute_index", 0)

    if progress["stage"] == "dict":
        dictionary = load_dictionary()
        while dict_index < len(dictionary):
            retry_queue = [item.code for item in load_retry()]
            if retry_queue:
                process_code(retry_queue[0], "dict", retry=True)
                continue
            code = dictionary[dict_index]
            process_code(code, "dict", index=dict_index)
            dict_index += 1

        progress.update({"stage": "brute", "brute_len": MIN_LEN, "brute_index": 0})
        save_progress(progress)
        brute_len = MIN_LEN
        brute_index = 0

    for length in range(brute_len, MAX_LEN + 1):
        index = brute_index if length == brute_len else 0

        while index < total_combinations(length):
            retry_queue = [item.code for item in load_retry()]
            if retry_queue:
                process_code(retry_queue[0], "brute", length=length, retry=True)
                continue
            code = brute_code_at(index, length)
            process_code(code, "brute", length=length, index=index)
            index += 1

        progress = load_progress()
        progress.update({"brute_len": length + 1, "brute_index": 0})
        save_progress(progress)

    logger.info("All done.")
