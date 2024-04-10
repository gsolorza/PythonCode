import psycopg2
from psycopg2 import extensions, errors
from pprint import pprint

# establishing the connection

TABLENAME: str = "NETWORKDEVICES"


class SQLPostgres:
    def __init__(
        self, host: str, database: str, user: str, password: str, port: str = "5432"
    ):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def __enter__(self):
        self.conn = psycopg2.connect(
            database=self.database,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
        )
        return self.conn.cursor()

    def __exit__(self, type: None, value: None, traceback: None):
        if self.conn:
            self.conn.commit()
            self.conn.close()


def queryDevice(
    cursor: extensions.cursor, tableName: str, query: str
) -> list[tuple[str]]:
    cursor.execute(query)
    result = cursor.fetchall()
    return [x for x in result]


def insertDevice(
    cursor: extensions.cursor,
    tableName: str,
    deviceInfo: list[tuple[str, str, str, str, str]],
) -> None:
    for deviceData in deviceInfo:
        deviceName, serialNumber, platform, version, ipAddress = deviceData
        insert: str = f"INSERT INTO {tableName} VALUES('{deviceName}', '{serialNumber}', '{platform}', '{version}', '{ipAddress}')"
        cursor.execute(insert)


def deleteDevice(
    cursor: extensions.cursor,
    tableName: str,
    devicesToDelete: tuple[str],
) -> None:
    delete: str = f"DELETE FROM {tableName} WHERE SERIAL in ('{devicesToDelete}')"
    cursor.execute(delete)


# def insertDb(cursor: extensions.cursor, query: str) ->)

with SQLPostgres(
    database="postgres",
    user="postgres",
    password="postgres",
    host="127.0.0.1",
    port="5432",
) as cursor:
    # Doping EMPLOYEE table if already exists.

    # cursor.execute("DROP TABLE IF EXISTS NETWORKDEVICES")
    # cursor.execute(
    #     "INSERT INTO NETWORKDEVICES VALUES('rt1', 'SL410XCA', 'C1111-8P', '16.6.7', '10.253.8.100')"
    # )
    # Creating table as per requirement
    createTable = f"""CREATE TABLE IF NOT EXISTS {TABLENAME}(
    DEVICE_NAME VARCHAR(20) NOT NULL,
    SERIAL VARCHAR(20) NOT NULL UNIQUE PRIMARY KEY,
    PLATFORM VARCHAR(20) NOT NULL,
    VERSION VARCHAR(20) NOT NULL,
    IP_ADDRESS VARCHAR(20) NOT NULL UNIQUE
    )"""
    # print(type(cursor))
    # cursor.execute(sql)
    cursor.execute(createTable)
    query = "SELECT * FROM NETWORKDEVICES"
    try:
        pprint(queryDevice(cursor, TABLENAME, query))
        deviceInfo = [("rt1", "SL410XCA", "C1111-8P", "16.6.7", "10.253.8.100")]
        insertDevice(cursor, TABLENAME, deviceInfo)
    except errors.Error as error:
        print(error)
    # pprint(cursor.fetchall())
