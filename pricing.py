from modules.storage import read_json, write_json, update_item, find_by_key
from modules.models import gen_id, now_iso

PRICING_FILE = 'pricing.json'


def get_pricing():
    data = read_json(PRICING_FILE)
    if not data:
        # default
        default = [{
            'pricing_id': gen_id('PR'),
            'type': 'default',
            'base_rate_hourly': 10.0,
            'base_rate_daily': 100.0,
            'updated_on': now_iso()
        }]
        write_json(PRICING_FILE, default)
        return default[0]
    return data[0]


def update_pricing(base_hourly: float, base_daily: float):
    pricing = get_pricing()
    pricing['base_rate_hourly'] = base_hourly
    pricing['base_rate_daily'] = base_daily
    pricing['updated_on'] = now_iso()
    update_item(PRICING_FILE, 'pricing_id', pricing['pricing_id'], pricing)
    return pricing

def compute_cost(duration_hours: float, duration_days: int, bike_rates: dict=None) -> float:
    # duration_days and duration_hours are mutually exclusive in most flows; support both
    p = get_pricing()
    # bike_rates can override base rates (rent_hourly/rent_daily on bike record)
    if bike_rates:
        h_rate = bike_rates.get('rent_hourly', p['base_rate_hourly'])
        d_rate = bike_rates.get('rent_daily', p['base_rate_daily'])
    else:
        h_rate = p['base_rate_hourly']
        d_rate = p['base_rate_daily']

    cost = 0.0
    if duration_days and duration_days > 0:
        cost += duration_days * d_rate
    if duration_hours and duration_hours > 0:
        # hourly billed fractionally
        cost += duration_hours * h_rate
    return round(cost, 2)
