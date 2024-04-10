from typing import Any
from pydantic import BaseModel
from datetime import datetime

class DataGroup(BaseModel):
    syslog_data: list[int]

class TimeGroup(BaseModel):
    date: list[int]
    time: list[int]
    missing_data: dict
    format: str

# Information we can gather vendor agnostic
class BaseSyslog(BaseModel):
    vendor: str
    device_model: str
    pattern: str
    type: int
    date_group: TimeGroup
    data_group: DataGroup

class SyslogData(BaseModel):
    timestamp: str
    syslog_data: str
    device_ip: str






