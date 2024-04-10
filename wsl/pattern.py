from pymongo import MongoClient
from schema import BaseSyslog, TimeGroup, DataGroup
from datetime import datetime
from pprint import pprint

client = MongoClient("10.100.1.190", 27017)

db = client.syslogdb
pattern = db.pattern
HOST = "0.0.0.0"
PORT = 514

pattern_list = [BaseSyslog(
        vendor= "Global",
        device_model= "Global",
        pattern= r"<\d+>:?(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{1,2})\s+(\d{2}):(\d{2}):(\d{2})\s+(.*)",
        type=1,
        date_group=TimeGroup
        (
            date=[1,2],
            time=[3,4,5],
            missing_data={
                "0": str(datetime.now().year)
            },
            format="%Y-%b-%d %H:%M:%S"
        ),
        data_group=DataGroup
        (
            syslog_data=[6]
        )
    ),
        BaseSyslog(
        vendor= "Global",
        device_model= "Global",
        pattern= r"<\d+>(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{1,2})\s+(\d{4})\s+(\d{2}):(\d{2}):(\d{2})\s+(.*)",
        type=999,
        date_group=TimeGroup
        (
            date=[3,1,2],
            time=[4,5,6],
            missing_data={
            },
            format="%Y-%b-%d %H:%M:%S"
        ),
        data_group=DataGroup
        (
            syslog_data=[7]
        )
    )
    ,
        BaseSyslog(
        vendor= "Fortinet",
        device_model= "Fortigate",
        pattern= r"<\d+>date=(\d{4})-(\d{2})-(\d{2})\s+time=(\d{2}):(\d{2}):(\d{2})\s+(.*)",
        type=1,
        date_group=TimeGroup
        (
            date=[1,2,3],
            time=[4,5,6],
            missing_data={
            },
            format="%Y-%m-%d %H:%M:%S"
        ),
        data_group=DataGroup
        (
            syslog_data=[7]
        )
    )
]

try:
    for syslog_pattern in pattern_list:
        pattern.insert_one(syslog_pattern.model_dump())
except Exception as error:
    print(error)

for pat in pattern.find():
    pprint(pat)
