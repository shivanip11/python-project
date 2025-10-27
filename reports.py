from modules.storage import read_json, append_item
from modules.models import gen_id, now_iso

REPORTS_FILE = 'reports.json'


def list_reports():
    return read_json(REPORTS_FILE)


def save_report(payload: dict):
    payload.update({'report_id': gen_id('R'), 'generated_on': now_iso()})
    append_item(REPORTS_FILE, payload)
    return payload
