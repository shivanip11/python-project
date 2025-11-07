from collections import Counter
from modules.models import now_iso
from modules.storage import read_json
from modules.storage import read_json, write_json, append_item, find_by_key, update_item, delete_item
from modules.models import gen_id, now_iso
from modules.utilities import print_table

BIKES_FILE = 'bikes.json'
USERS_FILE = 'users.json'
RENTALS_FILE = 'rentals.json'
REPORTS_FILE = 'reports.json'
PRICING_FILE = 'pricing.json'


def list_bikes():
    bikes = read_json(BIKES_FILE)
    print_table(bikes, headers=['bike_id', 'model', 'type', 'rent_hourly', 'rent_daily', 'availability'])
    return bikes


def add_bike(model: str, typ: str, rent_hourly: float = None, rent_daily: float = None, availability: bool = True):
   
    pricings = read_json(PRICING_FILE)
    base_hourly, base_daily = None, None

    for p in pricings:
        if p.get("type", "").lower() == typ.lower():
            base_hourly = p.get("base_rate_hourly")
            base_daily = p.get("base_rate_daily")
            break

    if base_hourly is not None and base_daily is not None:
        if rent_hourly is None:
            rent_hourly = base_hourly
        if rent_daily is None:
            rent_daily = base_daily
    else:
        if rent_hourly is None or rent_daily is None:
            raise ValueError(
                f"No pricing policy found for type '{typ}'. Please define it in pricing.json first.")

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
    bikes = read_json(BIKES_FILE)
    rentals = read_json(RENTALS_FILE)

    if not rentals:
        print("\nNo rentals found.")
        return

    
    rented_bikes = [r['bike_id']
                    for r in rentals if r.get('status') in ('active', 'closed')]
    if rented_bikes:
        count = Counter(rented_bikes)
        max_rent = max(count.values())
        most_rented_bikes = [{"bike_id": b, "times_rented": c}
                             for b, c in count.items() if c == max_rent]
    else:
        most_rented_bikes = []

   
    total_revenue = sum(float(r.get('cost', 0) or 0)
                        for r in rentals if r.get('status') == 'closed')

    
    pending_returns = [r for r in rentals if r.get('status') == 'active']

    
    print("\n==== RENTAL REPORT ====")
    

    print("Most Rented Bike(s):")
    if most_rented_bikes:
        print_table(most_rented_bikes, headers=['bike_id', 'times_rented'])
    else:
        print("<none>")

    print(f"\nTotal Revenue: ₹{total_revenue:.2f}")

    print("\nPending Returns:")
    if pending_returns:
        print_table(pending_returns, headers=[
                    'rental_id', 'bike_id', 'user_id', 'status'])
    else:
        print("<none>")

    report_entry = {
        "report_id": gen_id("R"),
        "type": "basic",
        "parameters": {
            "most_rented_bikes": [b["bike_id"] for b in most_rented_bikes],
            "times_rented": most_rented_bikes[0]["times_rented"] if most_rented_bikes else 0,
            "total_revenue": total_revenue,
            "pending_returns": len(pending_returns)
        },
        "generated_on": now_iso()
    }

    append_item(REPORTS_FILE, report_entry)

    print("\nReport generation complete.")
