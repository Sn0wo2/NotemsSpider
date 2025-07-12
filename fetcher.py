import logging

from curl_cffi import requests as cffi_requests
from lxml import html

from config import BASE_URL, IMPERSONATE
from db import get_session
from db_model import Result

logger = logging.getLogger(__name__)


def save_result(code, content):
    with get_session() as session:
        if not session.query(Result).filter_by(code=code).first():
            session.add(Result(code=code, content=content.strip()))
            session.commit()


def fetch_and_extract(code):
    url = BASE_URL + code
    try:
        r = cffi_requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115 Safari/537.36"
            },
            impersonate=IMPERSONATE,
            timeout=10,
        )

        if r.status_code == 200:
            tree = html.fromstring(r.text)
            found = False
            for t in tree.xpath("//textarea"):
                if t.text and t.text.strip():
                    logger.info(f"Found: {url}")
                    save_result(code, t.text)
                    found = True
                    break
            if not found:
                logger.info(f"No content: {url}")
        else:
            logger.warning(f"Status {r.status_code}: {url}")
        return True, None
    except Exception as e:
        logger.error(f"Error fetching {url}: {e}", exc_info=True)
        return False, code
