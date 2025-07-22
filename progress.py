import logging

from config import MIN_LEN, MAX_LEN
from db import get_read_session, get_write_session
from db_model import Progress, Result
from utils import (
    load_dictionary_cached,
    total_brute_combinations,
    total_combinations,
    get_code_index,
)

logger = logging.getLogger(__name__)


def init_progress():
    with get_write_session() as session:
        if not session.query(Progress).first():
            session.add(Progress(stage="dict"))


def load_progress():
    with get_read_session() as session:
        p = session.query(Progress).first()
        return {
            "stage": p.stage,
            "dict_index": p.dict_index,
            "brute_len": p.brute_len,
            "brute_index": p.brute_index,
        }


def save_progress(state):
    with get_write_session() as session:
        p = session.query(Progress).first()
        p.stage = state["stage"]
        p.dict_index = state["dict_index"]
        p.brute_len = state["brute_len"]
        p.brute_index = state["brute_index"]


def show_progress():
    progress = load_progress()
    stage = progress.get("stage", "dict")

    dict_total = len(load_dictionary_cached())
    brute_total = total_brute_combinations(MIN_LEN, MAX_LEN)
    total_tasks = dict_total + brute_total

    completed_tasks = 0
    if stage == "dict":
        dict_index = progress.get("dict_index", 0)
        completed_tasks = dict_index
    elif stage == "brute":
        completed_tasks = dict_total
        brute_len = progress.get("brute_len", MIN_LEN)
        brute_index = progress.get("brute_index", 0)

        for length in range(MIN_LEN, brute_len):
            completed_tasks += total_combinations(length)

        completed_tasks += brute_index

    percentage = (completed_tasks / total_tasks) * 100
    print(f"Progress: {completed_tasks}/{total_tasks} ({percentage:.4f}%)")


def sync_progress():
    with get_write_session() as session:
        last_result = session.query(Result).order_by(Result.id.desc()).first()
        if not last_result:
            logger.info("No results found, skipping progress sync.")
            return

        p = session.query(Progress).first()
        if not p:
            logger.error("Progress not initialized, cannot sync.")
            return

        progress = {
            "stage": p.stage,
            "dict_index": p.dict_index,
            "brute_len": p.brute_len,
            "brute_index": p.brute_index,
        }

        dictionary = load_dictionary_cached()
        code_info = get_code_index(last_result.code, dictionary, MIN_LEN)
        if not code_info:
            logger.warning(
                f"Could not determine index for code '{last_result.code}'. Skipping sync."
            )
            return

        res_stage, res_len, res_index = code_info
        prog_stage = progress["stage"]

        is_behind = (
            (prog_stage == "dict" and res_stage == "brute")
            or (
                prog_stage == "dict"
                and res_stage == "dict"
                and progress.get("dict_index", 0) <= res_index
            )
            or (
                prog_stage == "brute"
                and res_stage == "brute"
                and (progress.get("brute_len", MIN_LEN), progress.get("brute_index", 0))
                <= (res_len, res_index)
            )
        )

        if is_behind:
            logger.info(
                f"Progress is behind. Syncing based on last result code: {last_result.code}"
            )
            new_progress_state = {"stage": res_stage}
            if res_stage == "dict":
                new_progress_state["dict_index"] = res_index + 1
                new_progress_state["brute_len"] = progress.get("brute_len", MIN_LEN)
                new_progress_state["brute_index"] = progress.get("brute_index", 0)
            else:  # brute
                new_progress_state["dict_index"] = len(dictionary)
                new_progress_state["brute_len"] = res_len
                new_progress_state["brute_index"] = res_index + 1

            p.stage = new_progress_state["stage"]
            p.dict_index = new_progress_state["dict_index"]
            p.brute_len = new_progress_state["brute_len"]
            p.brute_index = new_progress_state["brute_index"]

            logger.info(f"Progress synced to: {new_progress_state}")
        else:
            logger.info("Progress is up-to-date.")
