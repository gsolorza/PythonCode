#!/usr/bin/env python3

import psycopg2
from datetime import datetime

con = psycopg2.connect(database="sdwan", user="postgres", password="GEO789**", host="127.0.0.1", port="5432")
cur = con.cursor()

date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

cur.execute("""
    CREATE TABLE IF NOT EXISTS people (
        time TIMESTAMP NOT NULL,
        firstname VARCHAR (255) NOT NULL,
        lastname VARCHAR (255) NOT NULL,
        age INT NOT NULL,
        description VARCHAR (255) DEFAULT 'description'
)
""")

cur.execute(f"INSERT INTO people (time, firstname, lastname, age) VALUES ('{date}', 'George', 'Solorzano', 31)")

con.commit()
con.close()






