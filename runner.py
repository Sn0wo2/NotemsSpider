import logging
import random
import sys
import time

from config import DELAY_RANGE, MIN_LEN, MAX_LEN, MAX_RETRIES
from fetcher import fetch_and_extract
from progress import (
    init_progress,
    load_progress,
    save_progress,
    show_progress,
    sync_progress,
)
from retry import load_retry, init_retry, save_retry, delete_retry, increment_retry
from utils import brute_code_at, total_combinations, load_dictionary_cached

logger = logging.getLogger(__name__)


def process_code(code, stage, length=0, index=0, retry_item=None):
    if stage != "retry":
        progress = load_progress()
        progress["stage"] = stage
        if stage == "dict":
            progress["dict_index"] = index + 1
        else:
            progress["brute_len"] = length
            progress["brute_index"] = index + 1
        save_progress(progress)

    success, failed_code = fetch_and_extract(code)
    if not success or failed_code:
        if stage == "retry":
            retries = increment_retry(code)
            if retries is not None and retries >= MAX_RETRIES:
                logger.info(f"Max retries reached for {code}, removing from queue.")
                delete_retry(code)
        else:
            save_retry(code)
    elif retry_item:
        logger.info(f"Delete retry: {code}")
        delete_retry(code)

    time.sleep(random.uniform(*DELAY_RANGE))


def run():
    if len(sys.argv) > 1 and sys.argv[1] == "progress":
        show_progress()
        return

    init_progress()
    sync_progress()
    init_retry()

    while True:
        retry_queue = load_retry()
        if retry_queue:
            logger.info(
                f"Processing {len(retry_queue)} items from the high-priority retry queue..."
            )
            for item in retry_queue:
                process_code(item.code, "retry", retry_item=item)
            continue

        progress = load_progress()
        stage = progress.get("stage", "dict")

        if stage == "dict":
            dictionary = load_dictionary_cached()
            dict_index = progress.get("dict_index", 0)

            if dict_index < len(dictionary):
                code = dictionary[dict_index]
                process_code(code, "dict", index=dict_index)
                continue
            else:
                logger.info("Dictionary scan complete. Switching to brute-force mode.")
                progress.update(
                    {"stage": "brute", "brute_len": MIN_LEN, "brute_index": 0}
                )
                save_progress(progress)
                continue

        if stage == "brute":
            brute_len = progress.get("brute_len", MIN_LEN)
            brute_index = progress.get("brute_index", 0)

            if brute_len > MAX_LEN:
                logger.info("All tasks and retries are complete.")
                break

            if brute_index < total_combinations(brute_len):
                code = brute_code_at(brute_index, brute_len)
                process_code(code, "brute", length=brute_len, index=brute_index)
            else:
                logger.info(f"Brute-force for length {brute_len} complete.")
                progress.update({"brute_len": brute_len + 1, "brute_index": 0})
                save_progress(progress)
            continue

    logger.info("All done.")


if __name__ == "__main__":
    run()
