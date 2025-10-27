from tabulate import tabulate


def pause():
    input('\nPress Enter to continue...')


def clear_screen():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def print_table(list_of_dicts, headers=None):
    if not list_of_dicts:
        print('\n<no records>')
        return
    if headers is None:
        headers = list(list_of_dicts[0].keys())
    rows = [[item.get(h, '') for h in headers] for item in list_of_dicts]
    print('\n' + tabulate(rows, headers=headers, tablefmt='grid'))
