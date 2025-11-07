from modules.utilities import clear_screen, pause
from modules.admin import list_bikes, add_bike, remove_bike, view_rentals, change_rental_status, generate_basic_reports
from modules.user import register_user, login_user, list_available_bikes, rent_bike, return_bike, rental_history
from modules.pricing import get_pricing, update_pricing

ADMINS_FILE = 'admin.json'
BIKES_FILE = 'bikes.json'
USERS_FILE = 'users.json'
RENTALS_FILE = 'rentals.json'
REPORTS_FILE = 'reports.json'

ADMIN_PASS = 'admin123'  ###################imp

def admin_menu():
    while True:
        clear_screen()
        print('--- Admin Menu ---')
        print('1. Add Bike')
        print('2. Update Bike')
        print('3. Delete Bike')
        print('4. View Bikes & Availability')
        print('5. Manage Rentals')
        print('6. Manage Pricing')
        print('7. Generate Reports')
        print('8. Logout')
        choice = input('> ').strip()
        if choice == '1':
            model = input('Model: ')
            typ = input('Type: ')
            hr = input('Hourly rate (blank for default): ')
            dy = input('Daily rate (blank for default): ')
            hr_val = float(hr) if hr else None
            dy_val = float(dy) if dy else None
            try:
                b = add_bike(model, typ, hr_val, dy_val)
                print('\nAdded:', b)
            except Exception as e:
                print('Error:', e)
            pause()

        elif choice == '2':
            bid = input('bike_id: ')
            print('Enter new values (leave blank to keep)')
            model = input('Model: ')
            typ = input('Type: ')
            hr = input('Hourly rate: ')
            dy = input('Daily rate: ')
            updates = {}
            if model:
                updates['model'] = model
            if typ:
                updates['type'] = typ
            if hr:
                updates['rent_hourly'] = float(hr)
            if dy:
                updates['rent_daily'] = float(dy)
            ok = update_bike(bid, **updates)
            print('Updated' if ok else 'Not found')
            pause()

        elif choice == '3':
            bid = input('bike_id to delete: ')
            ok = remove_bike(bid)
            print('Deleted' if ok else 'Not found')
            pause()

        elif choice == '4':
            list_bikes()
            pause()

        elif choice == '5':
            print('\n1. View Rentals')
            print('2. Approve/Close Rental (enter rental id and status)')
            c = input('> ')
            if c == '1':
                view_rentals()
                pause()
            elif c == '2':
                rid = input('rental_id: ')
                st = input('status (active/closed): ')
                ok = change_rental_status(rid, st)
                print('Done' if ok else 'Not found')
                pause()

        elif choice == '6':
            from modules.pricing import update_pricing
            update_pricing()
            pause()

        elif choice == '7':
            print('\nGenerating report...')
            generate_basic_reports() 
            pause()

        elif choice == '8':
            break

        else:
            print('Invalid option')
            pause()


def user_menu(user_id: str):
    while True:
        clear_screen()
        print('--- User Menu ---')
        print('1. View Available Bikes')
        print('2. Rent a Bike')
        print('3. Return a Bike')
        print('4. View Rental History')
        print('5. Logout')
        c = input('> ').strip()
        if c == '1':
            list_available_bikes()
            pause()
        elif c == '2':
            list_available_bikes()
            bid = input('Enter bike_id to rent: ')
            typ = input('Rent by hours (h) or days (d)? ')
            if typ.lower().startswith('h'):
                hrs = float(input('Hours (can be decimal): '))
                rental = rent_bike(user_id, bid, hours=hrs)
                print('\nRented:', rental)
            else:
                days = int(input('Days: '))
                rental = rent_bike(user_id, bid, days=days)
                print('\nRented:', rental)
            pause()
        elif c == '3':
            rid = input('Enter rental_id to return: ')
            try:
                ret = return_bike(rid)
                print('\nReturned:', ret)
            except Exception as e:
                print('Error:', e)
            pause()
        elif c == '4':
            rental_history(user_id)
            pause()
        elif c == '5':
            break
        else:
            print('Invalid choice')
            pause()


def main_menu():
    while True:
        clear_screen()
        print('=== Bike Rental Management System ===')
        print('1. Admin Login')
        print('2. User Login')
        print('3. Register as New User')
        print('4. Exit')
        ch = input('> ').strip()
        if ch == '1':
            pw = input('Enter admin password: ')
            if pw == ADMIN_PASS:
                admin_menu()
            else:
                print('Wrong password')
                pause()
        elif ch == '2':
            uid = input('Enter user_id: ')
            u = login_user(uid)
            if u:
                user_menu(uid)
            else:
                print('User not found')
                pause()
        elif ch == '3':
            name = input('Name: ')
            age = int(input('Age: '))
            lic = input('License no: ')
            contact = input('Contact: ')
            u = register_user(name, age, lic, contact)
            print('\nRegistered user:')
            print(u)
            pause()
        elif ch == '4':
            print('Thank You for using our Bike Rental Service')
            break
        else:
            print('Invalid')
            pause()


if __name__ == '__main__':
    main_menu()


