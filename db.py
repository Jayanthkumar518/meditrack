import pymysql

def get_connection():
    return pymysql.connect(
        host="my-database.c9gayi8ggbbd.ap-south-1.rds.amazonaws.com",
        user="admin",
        password="jayanth123",
        database="stdmanagement",
        cursorclass=pymysql.cursors.DictCursor
    )