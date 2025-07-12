from db import get_session
from db_model import Progress


def init_progress():
    with get_session() as session:
        if not session.query(Progress).first():
            session.add(Progress(stage="dict"))
            session.commit()


def load_progress():
    with get_session() as session:
        p = session.query(Progress).first()
        return {
            "stage": p.stage,
            "dict_index": p.dict_index,
            "brute_len": p.brute_len,
            "brute_index": p.brute_index,
        }


def save_progress(state):
    with get_session() as session:
        p = session.query(Progress).first()
        p.stage = state["stage"]
        p.dict_index = state["dict_index"]
        p.brute_len = state["brute_len"]
        p.brute_index = state["brute_index"]
        session.commit()
