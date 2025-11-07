from modules.storage import read_json, write_json, update_item, find_by_key
from modules.models import gen_id, now_iso

PRICING_FILE = 'pricing.json'


def get_pricing():
    data = read_json(PRICING_FILE)
    if not data:
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


def update_pricing():
    pricings = read_json(PRICING_FILE)
    if not pricings:
        print(" No pricing records found")
        return None

    print("\nAvailable Pricing Records:")
    for p in pricings:
        print(
            f"  {p['pricing_id']} | {p['type']} | Hourly: {p['base_rate_hourly']} | Daily: {p['base_rate_daily']}")

    chosen_id = input("\nEnter pricing_id to update: ").strip()
    selected = next(
        (p for p in pricings if p['pricing_id'] == chosen_id), None)

    if not selected:
        print(" Invalid pricing_id.")
        return None

    hh = input("New hourly rate (blank to keep current): ").strip()
    dd = input("New daily rate (blank to keep current): ").strip()

    if hh:
        selected['base_rate_hourly'] = float(hh)
    if dd:
        selected['base_rate_daily'] = float(dd)
    selected['updated_on'] = now_iso()

    update_item(PRICING_FILE, 'pricing_id', chosen_id, selected)
    print(f"\n Pricing '{chosen_id}' updated successfully.")
    return selected

def compute_cost(duration_hours: float, duration_days: int, bike_rates: dict=None) -> float:
    p = get_pricing()
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
        cost += duration_hours * h_rate
    return round(cost, 2)
