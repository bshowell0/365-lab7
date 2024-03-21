from . import printer, validate
from datetime import datetime

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

def fr2(cursor):
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
                    (res.CheckIn < %s AND res.Checkout >= %s)
            )
            AND r.maxOcc >= %s
    """
    params = [
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

    print(query, params)
    cursor.execute(query, params)


    result = cursor.fetchall()
    if result != []:
        return printer.fr2_res(cursor, result, choices)
    else:
        return fr2_res_empty(cursor, choices)

def fr2_res_update(cursor, choices, df):
    try:
        total_nights = (datetime.strptime(choices["end"], "%Y-%m-%d") - datetime.strptime(choices["start"], "%Y-%m-%d")).days
        query = """INSERT INTO lab7_reservations (Room, CheckIn, Checkout, Rate, LastName, FirstName, Adults, Kids)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"""
        params = [
            df["RoomCode"],
            choices["start"],
            choices["end"],
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

def fr2_res_empty(cursor, choices):
    pass