import os
import pandas as pd
from datetime import datetime, timedelta
from decimal import Decimal
from . import request, validate


pd.set_option('display.max_columns', None)
try:
    terminal_width = os.get_terminal_size().columns
    pd.set_option('display.width', terminal_width)
except OSError:
    pass

def welcome():
    try:
        terminal_height = os.get_terminal_size().lines - 1
    except OSError:
        terminal_height = 100
    print("\n" * terminal_height + "\033[H\033[J", end="")
    print("Welcome to the Hotel Reservation System!")

def invalid():
    print("Invalid input.\nType the code, full name, or underlined portion.\nE.g. 'FR1', 'Rooms and Rates', 'Rooms', or 'Rates'.\nCase insensitive.\n'Q' or 'Quit' to exit.")

def usr(extra=""):
    f = {"u": "\033[4m", "r": "\033[0m"}  # format: [underline, reset]
    spiel = (
        "Please select an option:\n\n"
        f"FR1: {f['u']}Rooms{f['r']} and {f['u']}Rates{f['r']}\n"
        f"FR2: {f['u']}Res{f['r']}ervations\n"
        f"FR3: Reservation {f['u']}Cancel{f['r']}lation\n"
        f"FR4: {f['u']}Detail{f['r']}ed Reservation {f['u']}Info{f['r']}rmation\n"
        f"FR5: {f['u']}Rev{f['r']}enue\n"
        f"{f['u']}Q{f['r']}uit\n"
    )
    usr = input(extra + spiel).lower()
    print("\033[H\033[J", end="")
    return usr


def fr1_res(data):
    df = pd.DataFrame(data, columns=["RoomCode", "RoomName", "Beds", "BedType", "MaxOcc", "BasePrice", "Decor", "PopularityScore", "NextAvailableCheckIn", "LengthOfStay", "CheckoutDate"])
    df.index += 1
    print(df)

def fr2_req():
    disp = [
        "First name: ",
        "Last name: ",
        "Room code (“Any” to indicate no preference): ",
        "Bed type (“Any” to indicate no preference): ",
        "Begin date of stay (YYYY-MM-DD): ",
        "End date of stay (YYYY-MM-DD): ",
        "Number of children: ",
        "Number of adults: "
    ]
    print("Please enter the following information to make a reservation:\n", "\n".join(disp), sep="\n")
    options = ["first", "last", "room", "bed", "start", "end", "children", "adults"]
    choices = {}
    for i, option in enumerate(options):
        choices[option] = input(f"\033[0m{disp[i]}\033[4m") if i > 0 else input("\033[3;13H\033[4m")
    print("\033[0m\033[H\033[J", end="")
    return choices

def fr2_res(cursor, data, choices):
    start_date = datetime.strptime(choices['start'], '%Y-%m-%d').date()
    end_date = datetime.strptime(choices['end'], '%Y-%m-%d').date()
    num_weekdays = 0
    num_weekends = 0
    for i in range((end_date - start_date).days):
        if (start_date + timedelta(days=i)).weekday() < 5:
            num_weekdays += 1
        else:
            num_weekends += 1
    df = pd.DataFrame(data, columns=["RoomCode", "RoomName", "Beds", "BedType", "MaxOcc", "BasePrice", "Decor"])
    df['CheckIn'] = choices['start']
    df['CheckOut'] = choices['end']
    df["TotalCost"] = num_weekdays * df['BasePrice'] + num_weekends * df['BasePrice'] * Decimal('1.1')
    df["TotalCost"] = df["TotalCost"].map("{:.2f}".format)
    df.index += 1
    print(df)
    num_selected = None
    while num_selected is None or (num_selected.isdigit() and not (df.index.start <= int(num_selected) < df.index.stop) and int(num_selected) != 0):
        if num_selected is not None:
            print("Invalid input. Please enter the number of the room you'd like to reserve, or 0 to cancel.")
        num_selected = input("Choose the number of the room you'd like to reserve, or 0 to cancel: ")
    print("\033[H\033[J", end="")
    num_selected = int(num_selected)
    if num_selected == 0:
        return (False, [])
    # # failed experiment
    # print(df[:num_selected])
    # print("\033[92m", '\n'.join(df[num_selected:num_selected+1].to_string().split('\n')[1:]), "\033[0m", sep="")
    # print('\n'.join(df[num_selected+1:].to_string().split('\n')[1:]))

    if not request.fr2_res_update(cursor, choices, df.loc[num_selected]):
        print("Reservation failed. Please try again.")
        return (False, [])
    chosen_room = df[num_selected-1:num_selected].to_string().split('\n')
    print(f"{chosen_room[0]}\n\033[92m{chosen_room[1]}\033[0m\n")
    print("Your reservation under the name of", choices["first"], choices["last"], "for room", df.loc[num_selected, "RoomCode"], "has been made for", choices["start"], "until", choices["end"])
    return (True, df.loc[num_selected])

def fr2_empty_res(cursor, df, choices):

    def calculate_total_cost(row):
        start_date = datetime.strptime(row['CheckIn'], '%Y-%m-%d').date()
        end_date = datetime.strptime(row['CheckOut'], '%Y-%m-%d').date()
        num_weekdays = 0
        num_weekends = 0
        for i in range((end_date - start_date).days):
            if (start_date + timedelta(days=i)).weekday() < 5:
                num_weekdays += 1
            else:
                num_weekends += 1
        total_cost = num_weekdays * row['BasePrice'] + num_weekends * row['BasePrice'] * Decimal('1.1')
        return "{:.2f}".format(total_cost)

    if df.empty:
        return (False, [])
    df['TotalCost'] = df.apply(calculate_total_cost, axis=1)

    print(df)
    num_selected = None
    while num_selected is None or (num_selected.isdigit() and not (df.index.start <= int(num_selected) < df.index.stop) and int(num_selected) != 0):
        if num_selected is not None:
            print("Invalid input. Please enter the number of the room you'd like to reserve, or 0 to cancel.")
        num_selected = input("Sorry, no rooms exactly fitting your criteria were found. Here are some options closely matching your request.\nChoose the number of the room you'd like to reserve, or 0 to cancel: ")
    print("\033[H\033[J", end="")
    num_selected = int(num_selected)
    if num_selected == 0:
        return (False, [])

    if not request.fr2_res_update(cursor, choices, df.loc[num_selected]):
        print("Reservation failed. Please try again.")
        return (False, [])
    chosen_room = df[num_selected-1:num_selected].to_string().split('\n')
    print(f"{chosen_room[0]}\n\033[92m{chosen_room[1]}\033[0m\n")
    print("Your reservation under the name of", choices["first"], choices["last"], "for room", df.loc[num_selected, "RoomCode"], "has been made for", df.loc[num_selected, 'CheckIn'], "until", df.loc[num_selected, 'CheckOut'])
    return (True, df.loc[num_selected])

def res_code(code):
    print(f"Your reservation code is {code}")

def fr2_failed():
    print("Sorry, there are no exact nor approximate reservations available matching your criteria.")


def fr3_req():
    res_num = None
    while not validate.fr3_req(res_num):
        if res_num is not None:
            print("Invalid input. Please enter the reservation code you'd like to cancel.")
        res_num = input("Please enter the reservation code you'd like to cancel: ")
    print("\033[H\033[J", end="")
    return res_num

def fr3_failed():
    print("Sorry, no reservation was found with that code.")

def fr3_confirm(code, data):
    print(f"Reservation {code}:")
    df = pd.DataFrame(data, columns=["CODE", "Room", "CheckIn", "Checkout", "Rate", "LastName", "FirstName", "Adults", "Kids"])
    print(df)
    f = {"u": "\033[4m", "r": "\033[0m"}  # format: [underline, reset]
    confirm = None
    while validate.fr3_confirm(confirm) is False:
        if confirm is not None:
            print(f"Invalid input. Please enter '{f['u']}Y{f['r']}es' or '{f['u']}N{f['r']}o'.")
        confirm = input(f"Are you sure you want to cancel this reservation? ({f['u']}Y{f['r']}es/{f['u']}N{f['r']}o): ").upper()
    print("\033[H\033[J", end="")
    return confirm[0] == "Y"



def fr5(result):
    df = pd.DataFrame(result, columns=["Room", "Rate", "CheckIn", "Checkout"])
    df['CheckIn'] = pd.to_datetime(df['CheckIn'])
    df['Checkout'] = pd.to_datetime(df['Checkout'])
    df['Date'] = df.apply(lambda row: pd.date_range(start=row['CheckIn'], end=row['Checkout'] - pd.Timedelta(days=1), freq='D'), axis=1)
    df = df.explode('Date')
    df['DailyRevenue'] = df['Rate']
    df['Month'] = df['Date'].dt.month
    # print("df:", df)
    # print("monthly revenue:", monthly_revenue)
    month_names = {
        1: 'January',
        2: 'February',
        3: 'March',
        4: 'April',
        5: 'May',
        6: 'June',
        7: 'July',
        8: 'August',
        9: 'September',
        10: 'October',
        11: 'November',
        12: 'December'
    }
    pivot = df.pivot_table(index='Room', columns='Month', values='DailyRevenue', aggfunc='sum', fill_value=0)
    pivot = pivot.rename(columns=month_names)
    pivot['Yearly Total'] = pivot.sum(axis=1)
    pivot.loc['Monthly Total'] = pivot.sum()
    pivot = pivot.round(0).astype(int)
    print(pivot)
