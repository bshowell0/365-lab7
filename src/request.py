from . import printer, validate

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
    query = f"""
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
                (res.CheckIn < '{choices["end"]}' AND res.Checkout > '{choices["start"]}')
        )
        AND r.maxOcc >= {int(choices["children"]) + int(choices["adults"])}
    """
    query += "   "
    if choices["room"] != 'ANY':
        query += f""" AND r.RoomCode = '{choices["room"]}'"""
    if choices["bed"] != 'ANY':
        query += f""" AND r.bedType = '{choices["bed"]}'"""
    query += "\nORDER BY r.basePrice;"

    print(query)

    cursor.execute(query)
    result = cursor.fetchall()
    if result != []:
        printer.fr2_res(result)
    else:
        fr2_res_empty(cursor, choices)

def fr2_res_empty(cursor, choices):
    pass