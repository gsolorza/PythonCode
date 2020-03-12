import re
from pprint import pprint
import pandas as pd

bp_test = {
    "Banners":
            [
                ("Banner Message of the day (MOTD)", r"banner\smotd", True, "bajo", "corto"),
                ("Banner Login", r"banner\slogin" ,True, "bajo", "corto"),
                ("Banner Exec", r"banner\sexec",True, "bajo", "corto")
            ],

    "Authentication, Authorization and Accouting (AAA)":
            [
                ("AAA Enable", r"aaa new-model", True, "bajo", "corto"),                    
                ("LOGIN Authentication", r"banner\sexec.*", True, "bajo", "corto"),                    
                ("EXEC Accounting", r"aaa accounting exec.*", True, "bajo", "corto"),                    
                ("COMMANDS Accounting", r"aaa accounting commands.*", True, "bajo", "corto"),                    
                ("EXEC Authorization", r"aaa accounting exec.*", True, "bajo", "corto"),                    
                ("COMMANDS Authorization", r"aaa accounting commands.*", True, "bajo", "corto")                
            ],

    "Comandos que deben ser evitados":
            [
                ("Password 7 in Line VTY", r"\spassword\s7\s\w+", False, "bajo", "corto"),
                ("Password 7 or 0 for Username", r"username\s.*password\s.*", False, "bajo", "corto"),
                ("http Enabled", r"^ip http server", False, "bajo", "corto"),
                ("Enable Password", r"^enable password\s\w+$", False, "bajo", "corto"),
                ("Generic user names created", r"^username\scisco|username\sadmin", False, "bajo", "corto")
            ],
            
    "Line VTY":
            [
                ("SSH Only Access", r"\stransport input ssh$|\stransport input ssh\s$",True, "bajo", "corto"),
                ("EXEC Timeout", r"^\sexec-timeout.*",True, "bajo", "corto"),
                ("LOGGING Sync", r"logging synchronous",True, "bajo", "corto"),
                ("ACCESS-LIST for ssh", r"access-class.*\sin.*",True, "bajo", "corto")  
            ],

    "Logging":
            [
                ("Centralized Logging", r"logging host.*",True, "bajo", "corto"),                
                ("Logging Buffered", r"logging buffered.*",True, "bajo", "corto"),                
                ("Logging Source-Interface", r"logging source-interface\s.*",True, "bajo", "corto")            
            ],

    "Simple Network Management Protocol (SNMP)":
            [
                ("SNMP Server ACL", r"snmp-server community\s\w+\s(RO|RW)\s\w+$",True, "bajo", "corto"),
                ("SNMP Trap Source", r"snmp-server trap-source.*",True, "bajo", "corto")
            ],

    "Network Time Protocol (NTP)":
            [
                ("Timezone Configured", r"clock timezone\s.*", True, "bajo", "corto"),
                ("NTP server Configured", r"ntp\sserver\s[\d.]+.*", True, "bajo", "corto")
            ]     
}

with open("/home/gsolorza/PythonCode/Assessment/Salcobrand/cisco_ios/RTR_ANGAMOS01/show_run.log") as file:
    show_run = file.read()

df = {
    "Clasificacion": [],
    "Descripcion": [],
    "Impacto": [],
    "Workarround": [],
    "Evidencia": []
}


def find_re(regex, data):
    pattern = re.compile(regex, re.M|re.I)
    return pattern.findall(data)

for clasificacion in bp_test.keys():
    for bp, regex, should_match, impact, deadline in bp_test[clasificacion]:
        matches = find_re(regex, show_run)
        if should_match == True and matches:
            pass
        elif should_match == True and not matches:
            df["Clasificacion"].append(clasificacion)
            df["Descripcion"].append(bp)
            df["Impacto"].append(impact)
            df["Workarround"].append("Como best practice se debe configurar "+bp)
            df["Evidencia"].append(bp+" no encontrado")
        elif should_match == False and not matches:
            pass
        elif should_match == False and matches:
            df["Clasificacion"].append(clasificacion)
            df["Descripcion"].append(bp)
            df["Impacto"].append(impact)
            df["Workarround"].append("Como best practice se debe eliminar "+bp)
            df["Evidencia"].append(matches[0])
        
dataframe = pd.DataFrame(df)
print(dataframe)