from modules.storage import read_json, write_json, append_item, find_by_key, update_item, delete_item
from modules.models import gen_id, now_iso
from modules.utils import print_table

BIKES_FILE = 'bikes.json'
USERS_FILE = 'users.json'
RENTALS_FILE = 'rentals.json'
REPORTS_FILE = 'reports.json'


def list_bikes():
    bikes = read_json(BIKES_FILE)
    print_table(bikes, headers=['bike_id', 'model', 'type', 'rent_hourly', 'rent_daily', 'availability'])
    return bikes


def add_bike(model: str, typ: str, rent_hourly: float, rent_daily: float, availability: bool = True):
    bike = {
        'bike_id': gen_id('B'),
        'model': model,
        'type': typ,
        'rent_hourly': float(rent_hourly),
        'rent_daily': float(rent_daily),
        'availability': bool(availability)
    }
    append_item(BIKES_FILE, bike)
    return bike
def update_bike(bike_id: str, **kwargs):
    bike = find_by_key(BIKES_FILE, 'bike_id', bike_id)
    if not bike:
        return False
    bike.update(kwargs)
    update_item(BIKES_FILE, 'bike_id', bike_id, bike)
    return True


def remove_bike(bike_id: str):
    return delete_item(BIKES_FILE, 'bike_id', bike_id)


def view_rentals():
    rentals = read_json(RENTALS_FILE)
    print_table(rentals, headers=['rental_id','user_id','bike_id','start_time','end_time','duration','cost','status'])
    return rentals


def change_rental_status(rental_id: str, status: str):
    rental = find_by_key(RENTALS_FILE, 'rental_id', rental_id)
    if not rental:
        return False
    rental['status'] = status
    update_item(RENTALS_FILE, 'rental_id', rental_id, rental)
    return True
def generate_basic_reports():
    # sample: most rented bikes, total revenue, pending returns
    rentals = read_json(RENTALS_FILE)
    bikes = read_json(BIKES_FILE)
    from collections import Counter
    rented = [r['bike_id'] for r in rentals if r.get('status') in ('active', 'closed')]
    most = Counter(rented).most_common(5)
    revenue = sum([float(r.get('cost',0) or 0) for r in rentals if r.get('status') == 'closed'])
    pending = [r for r in rentals if r.get('status') == 'active']
    report = {
        'report_id': gen_id('R'),
        'type': 'basic',
        'parameters': {},
        'generated_on': now_iso(),
        'most_rented': most,
        'total_revenue': revenue,
        'pending_returns': len(pending)
    }
    # append to reports file
    append_item(REPORTS_FILE, report)
    return report
