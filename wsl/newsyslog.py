import socket
from pymongo import MongoClient
import re
from datetime import datetime
from schema import BaseSyslog, SyslogData
from pprint import pprint

client = MongoClient("10.100.1.190", 27017)

db = client.syslogdb
# db.drop_collection("syslog")
syslog = db.syslog
pattern = db.pattern
HOST = "0.0.0.0"
PORT = 514

def check_datetime_format(timestamp: str, datetime_format: str):
    try:
        timezone = datetime.utcnow()
        timestamp = str(timezone.strptime(timestamp, datetime_format))
        return timestamp
    except ValueError:
        return None

def find_match(syslog_message, device_ip) -> SyslogData:
    # Define a regular expression pattern to match the timestamp
    # date_pattern_list = [
    #     r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}\b",
    #     r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2}\s+\d{4}\s+\d{2}:\d{2}:\d{2}\b",
    #     r"<(\d+)>date=(\d{4}-\d{2}-\d{2})\s+time=(\d{2}:\d{2}:\d{2})"
    #     # r"<(\d+)>(date=(\d{4}-\d{2}-\d{2}))\s+time=(\d{2}:\d{2}:\d{2})\s+devname=\"([^\"]+)\"\s+devid=\"([^\"]+)\"\s+eventtime=(\d+)\s+tz=\"([^\"]+)\"\s+logid=\"([^\"]+)\"\s+type=\"([^\"]+)\"\s+subtype=\"([^\"]+)\"\s+level=\"([^\"]+)\"\s+vd=\"([^\"]+)\"\s+srcip=(\d+\.\d+\.\d+\.\d+)\s+srcport=(\d+)\s+srcintf=\"([^\"]+)\"\s+srcintfrole=\"([^\"]+)\"\s+dstip=(\d+\.\d+\.\d+\.\d+)\s+dstport=(\d+)\s+dstintf=\"([^\"]+)\"\s+dstintfrole=\"\(\[\^\"\]\+\)\"\s+srccountry=\"\(\[\^\"\]\+\)\"\s+dstcountry=\"\(\[\^\"\]\+\)\"\s+sessionid=(\d+)\s+proto=(\d+)\s+action=\"\(\[\^\"\]\+\)\"\s+policyid=(\d+)\s+policytype=\"\(\[\^\"\]\+\)\"\s+service=\"\(\[\^\"\]\+\)\"\s+trandisp=\"\(\[\^\"\]\+\)\"\s+app=\"\(\[\^\"\]\+\)\"\s+duration=(\d+)\s+sentbyte=(\d+)\s+rcvdbyte=(\d+)\s+sentpkt=(\d+)\s+rcvdpkt=(\d+)\s+appcat=\"\(\[\^\"\]\+\)\">"
    # ]

    date_pattern_list = pattern.find().sort({"type": -1})
    for pattern_data in date_pattern_list:
        _pattern = BaseSyslog.model_validate(pattern_data)
        pattern_string = _pattern.pattern
        # Use re.search to find the timestamp in the message
        match = re.search(pattern_string, syslog_message)
        if match:
            # print(pattern_string)
            # print(syslog_message)
            try:
                date_group = _pattern.date_group
                data_group = _pattern.data_group
                date_list = [match.group(group) for group in date_group.date]
                for index, data in date_group.missing_data.items():
                    date_list.insert(int(index), data)
                date = "-".join(date_list)
                time = ":".join([match.group(group) for group in date_group.time])
                timestamp = f"{date} {time}"
                data = " ".join([match.group(group) for group in data_group.syslog_data])
                if check_datetime_format(timestamp, date_group.format) and data:
                    timestamp = check_datetime_format(timestamp, date_group.format)
                    syslog_data = SyslogData(
                    timestamp=timestamp,
                    syslog_data=data,
                    device_ip=device_ip
                )
                    
                    return syslog_data
            except Exception as error:
                print(error)
    return None
    




# print(db.list_collection_names())

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
    print(f"{HOST} Listening on port {PORT}")
    while True:
        data_bytes, ip = s.recvfrom(4096)
        data = data_bytes.decode("UTF-8", errors="ignore")
        device_ip = ip[0]
        print(data)
        syslog_data = find_match(data, device_ip)
        if syslog_data:
            syslog.insert_one(syslog_data.model_dump())
        if not data:
            break

# myquery = { "device_ip": "10.100.1.254" }

# syslog.delete_many(myquery)

# for syslog in syslog.find():
#     print(syslog
