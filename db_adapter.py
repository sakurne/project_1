import psycopg2
import settings


class DataBase:

    def __init__(self):
        self.connection = psycopg2.connect(
            database=settings.DB_NAME,
            user=settings.DB_LOGIN,
            password=settings.DB_PASSWORD,
            host=settings.DB_HOST,
            port=settings.DB_PORT
        )
        self.cursor = self.connection.cursor()
        
        
def get_clinics_for_prices(self):
    rows = self.get_rows(
        'SELECT DISTINCT u.username '
        'FROM au_user u '
        'JOIN doctors_user2 u2 ON u.id = u2.user_id '
        'JOIN doctors_lpu lpu ON lpu.owner_id = u2.id '
        'JOIN doctors_lpuphone lpu_p ON lpu_p.lpu_id=lpu.id  '
        'WHERE usertype = 3 '
        'AND is_active '
        'AND u2.balance > 400 '
        'AND lpu.express '
        'AND lpu.phone '
        'AND lpu_p.active '
        'AND NOT lpu.closed;'
    )
    res = []
    for row in rows:
        res.append(row[0])
    return res
