from . import printer, validate
from datetime import datetime, timedelta
import pandas as pd  #TODO remove

def fr1(cursor):
    request = (
        "WITH reservation_data AS ( "
          "SELECT  "
            "Room, "
            "COALESCE(ROUND(COUNT(DATEDIFF(CheckIn, Checkout))/180, 2), 0) AS PopularityScore, "
            "MIN(CASE WHEN Checkout >= CURDATE() THEN Checkout END) + INTERVAL 1 DAY AS NextAvailableCheckIn, "
            "MAX(CASE WHEN Checkout <= CURDATE() THEN Checkout END) AS LastCheckout "
          "FROM  "
            "lab7_reservations "
          "WHERE  "
            "CheckIn >= DATE_SUB(CURDATE(), INTERVAL 180 DAY) "
          "GROUP BY  "
            "Room "
        "), "
        "stay_data AS ( "
          "SELECT  "
            "Room, "
            "DATEDIFF(Checkout, CheckIn) AS LengthOfStay "
          "FROM  "
            "lab7_reservations "
          "WHERE  "
            "Checkout = (SELECT LastCheckout FROM reservation_data WHERE Room = lab7_reservations.Room) "
        ") "
        "SELECT  "
          "r.*,  "
          "res.PopularityScore, "
          "res.NextAvailableCheckIn, "
          "s.LengthOfStay, "
          "res.LastCheckout AS CheckoutDate "
        "FROM  "
          "lab7_rooms AS r "
        "LEFT JOIN  "
          "reservation_data AS res "
        "ON  "
          "r.RoomCode = res.Room "
        "LEFT JOIN  "
          "stay_data AS s "
        "ON  "
          "r.RoomCode = s.Room "
        "ORDER BY  "
          "res.PopularityScore DESC; "
    )
    cursor.execute(request)
    result = cursor.fetchall()
    printer.fr1_res(result)

def fr2(cursor, conn):
    choices = printer.fr2_req()
    choices = validate.fr2_req(choices)

    query = """
        SELECT
            r.RoomCode,
            r.RoomName,
            r.Beds,
            r.bedType,
            r.maxOcc,
            r.basePrice,
            r.decor
        FROM
            lab7_rooms AS r
        WHERE
            r.RoomCode NOT IN (
                SELECT
                    res.Room
                FROM
                    lab7_reservations AS res
                WHERE
                    (res.CheckIn < %s AND res.Checkout > %s) OR (res.CheckIn <= %s AND res.Checkout > %s)
            )
            AND r.maxOcc >= %s
    """
    params = [
        choices["end"],
        choices["start"],
        choices["end"],
        choices["start"],
        str(int(choices["children"]) + int(choices["adults"]))
    ]

    if choices["room"] != 'ANY':
        query += " AND r.RoomCode = %s"
        params.append(choices["room"])
    if choices["bed"] != 'ANY':
        query += " AND r.bedType = %s"
        params.append(choices["bed"])

    query += " ORDER BY r.basePrice;"

    cursor.execute(query, params)

    result = cursor.fetchall()
    if result != []:
        (success, df) = printer.fr2_res(cursor, result, choices)
    else:
        (success, df) = fr2_res_empty(cursor, choices)
    if success:
        conn.commit()
        printer.res_code(get_res_code(cursor, df))
    else:
        printer.fr2_failed()

def fr2_res_empty(cursor, choices):
    start_date = datetime.strptime(choices['start'], '%Y-%m-%d').date()
    end_date = datetime.strptime(choices['end'], '%Y-%m-%d').date()
    num_days = (end_date - start_date).days
    query2 = """
        SELECT
            NextCheckout,
            NextCheckIn
        FROM (
            SELECT
                MIN(res1.Checkout) AS NextCheckout,
                (SELECT MIN(res2.CheckIn) FROM lab7_reservations AS res2 WHERE res2.CheckIn > MIN(res1.Checkout) AND (res2.Room = %s OR %s = 'ANY')) AS NextCheckIn
            FROM
                lab7_reservations AS res1
            JOIN lab7_rooms AS rooms
            WHERE
                res1.Checkout > %s AND
                rooms.maxOcc >= %s AND
                (res1.Room = %s OR %s = 'ANY')
        ) AS subquery
        WHERE
            DATEDIFF(NextCheckIn, NextCheckout) >= %s
        ORDER BY NextCheckin
    """
    params2 = [choices["room"], choices["room"], choices["start"], str(int(choices["children"]) + int(choices["adults"])), choices["room"], choices["room"], num_days]
    cursor.execute(query2, params2)
    result2 = cursor.fetchall()
    old_dates = (choices["start"], choices["end"])
    new_dates = (result2[0][0].strftime("%Y-%m-%d"), (result2[0][0] + timedelta(days=num_days)).strftime("%Y-%m-%d"), result2[0][1].strftime("%Y-%m-%d"))
    choices["start"] = new_dates[0]
    choices["end"] = new_dates[1]
    query = """
        SELECT
            r.RoomCode,
            r.RoomName,
            r.Beds,
            r.bedType,
            r.maxOcc,
            r.basePrice,
            r.decor
        FROM
            lab7_rooms AS r
        WHERE
            r.RoomCode NOT IN (
                SELECT
                    res.Room
                FROM
                    lab7_reservations AS res
                WHERE
                    (res.CheckIn < %s AND res.Checkout > %s) OR (res.CheckIn <= %s AND res.Checkout > %s)
            )
            AND r.maxOcc >= %s
    """
    params = [
        choices["end"],
        choices["start"],
        choices["end"],
        choices["start"],
        str(int(choices["children"]) + int(choices["adults"]))
    ]


    if choices["room"] != 'ANY':
        query += " AND r.RoomCode = %s"
        params.append(choices["room"])
    if choices["bed"] != 'ANY':
        query += " AND r.bedType = %s"
        params.append(choices["bed"])

    query += " ORDER BY r.basePrice;"

    cursor.execute(query, params)

    result1 = cursor.fetchall()
    choices["start"] = old_dates[0]
    choices["end"] = old_dates[1]
    query = """
        SELECT
            r.RoomCode,
            r.RoomName,
            r.Beds,
            r.bedType,
            r.maxOcc,
            r.basePrice,
            r.decor
        FROM
            lab7_rooms AS r
        WHERE
            r.RoomCode NOT IN (
                SELECT
                    res.Room
                FROM
                    lab7_reservations AS res
                WHERE
                    (res.CheckIn < %s AND res.Checkout > %s) OR (res.CheckIn <= %s AND res.Checkout > %s)
            )
            AND r.maxOcc >= %s
        LIMIT 5
    """
    params = [
        choices["end"],
        choices["start"],
        choices["end"],
        choices["start"],
        str(int(choices["children"]) + int(choices["adults"]))
    ]
    cursor.execute(query, params)
    result2 = cursor.fetchall()
    df1 = pd.DataFrame(result1, columns=["RoomCode", "RoomName", "Beds", "BedType", "MaxOcc", "BasePrice", "Decor"])
    df1['CheckIn'] = new_dates[0]
    df1['CheckOut'] = new_dates[1]
    df2 = pd.DataFrame(result2, columns=["RoomCode", "RoomName", "Beds", "BedType", "MaxOcc", "BasePrice", "Decor"])
    df2['CheckIn'] = old_dates[0]
    df2['CheckOut'] = old_dates[1]
    df = pd.concat([df1, df2]).reset_index(drop=True)
    df.index += 1
    return printer.fr2_empty_res(cursor, df, choices)

def fr2_res_update(cursor, choices, df):
    try:
        total_nights = (datetime.strptime(df["CheckOut"], "%Y-%m-%d") - datetime.strptime(df["CheckIn"], "%Y-%m-%d")).days
        query = """INSERT INTO lab7_reservations (Room, CheckIn, Checkout, Rate, LastName, FirstName, Adults, Kids)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"""
        params = [
            df["RoomCode"],
            df["CheckIn"],
            df["CheckOut"],
            str(round(float(df["TotalCost"]) / total_nights, 2)),
            choices["last"],
            choices["first"],
            choices["adults"],
            choices["children"]
        ]
        cursor.execute(query, params)
        return True
    except:
        return False

def get_res_code(cursor, df):
    query = """
SELECT CODE
FROM lab7_reservations
WHERE Room = %s AND CheckIn = %s AND Checkout = %s
"""
    params = [df["RoomCode"], df["CheckIn"], df["CheckOut"]]
    cursor.execute(query, params)
    return cursor.fetchall()[0][0]


def fr3(cursor, conn):
    res_num = printer.fr3_req()
    # get reservation info
    query = "SELECT * FROM lab7_reservations WHERE CODE = %s"
    cursor.execute(query, [res_num])
    result = cursor.fetchall()
    if result == []:
        printer.fr3_failed()
        return
    if not printer.fr3_confirm(res_num, result):
        return
    query = "DELETE FROM lab7_reservations WHERE CODE = %s"
    cursor.execute(query, [res_num])
    conn.commit()
    print("Reservation", res_num, "cancelled.")

