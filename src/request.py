from . import printer

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
    printer.fr1(result)