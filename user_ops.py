from modules.storage import read_json, append_item, find_by_key, update_item
from modules.models import gen_id, now_iso, parse_iso
from modules.utils import print_table
from modules.pricing import compute_cost

USERS_FILE = 'users.json'
BIKES_FILE = 'bikes.json'
RENTALS_FILE = 'rentals.json'


def register_user(name: str, age: int, license_no: str, contact: str):
    user = {
        'user_id': gen_id('U'),
        'name': name,
        'age': int(age),
        'license_no': license_no,
        'contact': contact,
        'registered_on': now_iso()
    }
    append_item(USERS_FILE, user)
    return user


def login_user(user_id: str):
    return find_by_key(USERS_FILE, 'user_id', user_id)
def list_available_bikes(filter_type=None, filter_model=None):
    bikes = read_json(BIKES_FILE)
    available = [b for b in bikes if b.get('availability') in (True, 'True', 'true')]
    if filter_type:
        available = [b for b in available if b.get('type') == filter_type]
    if filter_model:
        available = [b for b in available if b.get('model') == filter_model]
    print_table(available, headers=['bike_id','model','type','rent_hourly','rent_daily'])
    return available
def rent_bike(user_id: str, bike_id: str, hours: float=None, days: int=None):
    bike = find_by_key(BIKES_FILE, 'bike_id', bike_id)
    if not bike:
        raise ValueError('Bike not found')
    if not bike.get('availability'):
        raise ValueError('Bike not available')
    # cost calculation
    cost = compute_cost(duration_hours=hours or 0.0, duration_days=days or 0, bike_rates=bike)
    rental = {
        'rental_id': gen_id('RE'),
        'user_id': user_id,
        'bike_id': bike_id,
        'start_time': now_iso(),
        'end_time': None,
        'duration': f"{days or 0} days, {hours or 0} hours",
        'cost': cost,
        'status': 'active'
    }
    # mark bike unavailable
    bike['availability'] = False
    update_item(BIKES_FILE, 'bike_id', bike_id, bike)
    append_item(RENTALS_FILE, rental)
    return rental

def return_bike(rental_id: str):
    rental = find_by_key(RENTALS_FILE, 'rental_id', rental_id)
    if not rental:
        raise ValueError('Rental not found')
    if rental.get('status') != 'active':
        raise ValueError('Rental is not active')
    # determine actual duration and cost: for simplicity, treat flat from stored cost
    # update end_time and status
    rental['end_time'] = now_iso()
    rental['status'] = 'closed'
    update_item(RENTALS_FILE, 'rental_id', rental_id, rental)
    # set bike available
    bike = find_by_key(BIKES_FILE, 'bike_id', rental['bike_id'])
    if bike:
        bike['availability'] = True
        update_item(BIKES_FILE, 'bike_id', bike['bike_id'], bike)
    return rental
def rental_history(user_id: str):
    rentals = read_json(RENTALS_FILE)
    my = [r for r in rentals if r.get('user_id') == user_id]
    print_table(my, headers=['rental_id','bike_id','start_time','end_time','duration','cost','status'])
    return my
