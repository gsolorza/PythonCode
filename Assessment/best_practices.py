import re
from pprint import pprint
import pandas as pd

bp_list = {"Banners":
            {
                "impacto": "bajo",
                "plazo": "corto",
                "should_match": True,
                "regex": 
                {
                    "Banner Message of the day (MOTD)": r"banner\smotd",
                    "Banner Login": r"banner\slogin",
                    "Banner Exec": r"banner\sexec"
                }
            
            },
        "Authentication, Authorization and Accouting":
            {
                "impacto": "medio",
                "plazo": "corto",
                "should_match": True,
                "regex": 
            
                {
                    "AAA Enable": r"aaa new-model",
                    "LOGIN Authentication": r"banner\sexec.*",
                    "EXEC Accounting": r"aaa accounting exec.*",
                    "COMMANDS Accounting": r"aaa accounting commands.*",
                    "EXEC Authorization": r"aaa accounting exec.*",
                    "COMMANDS Authorization": r"aaa accounting commands.*"
                }
            
            },
        "Line VTY":
            {
                "impacto": "low",
                "plazo": "medio",
                "should_match": True,
                "regex":
                {
                    "SSH Only Access": r"\stransport input ssh$|\stransport input ssh\s$",
                    "EXEC Timeout": r"^\sexec-timeout.*",
                    "LOGGING Sync": r"logging synchronous",
                    "ACCESS-LIST for ssh": r"access-class.*\sin.*"
                }
            
            },
        "Logging":  
            {
                "impacto": "low",
                "plazo": "medio",
                "should_match": True,
                "regex": 
                {
                    "Centralized Logging": r"logging host.*",
                    "Logging Buffered": r"logging buffered.*",
                    "Logging Source-Interface": r"logging source-interface\s.*"
                }
            },
        "Simple Network Management Protocol (SNMP)": 
            {
                "impacto": "low",
                "plazo": "medio",
                "regex":
                {
                    "SNMP Server ACL": r"snmp-server community\s\w+\s(RO|RW)\s\w+$",
                    "SNMP Trap Source": r"snmp-server trap-source.*"
                }  
            },
        "Network Time Protocol (NTP)": 
            {           
                "impacto": "low",
                "plazo": "medio",
                "should_match": True,
                "regex":  
                {
                    "Timezone Configured": r"clock timezone\s.*",
                    "NTP server Configured": r"ntp\sserver\s[\d.]+.*"
                }  
            },
        "Comandos que deben ser evitados":
            {
                "impacto": "low",
                "plazo": "medio",
                "should_match": False,
                "regex":
            
                {
                    "Password 7 in Line VTY": r"\spassword\s7\s\w+",
                    "Password 7 or 0 for Username": r"username\s.*password\s.*",
                    "http Enabled": r"^ip http server",
                    "Enable Password": r"^enable password\s\w+$",
                    "Generic user names created": r"^username\scisco|username\sadmin"
                }  
            }
}

# for categoria, bp_attributes in bp_list.items():
#     for key, value in bp_attributes.items():
#         if key == "regex":
#             for description, reg in value.items():
#                 pattern = re.compile(reg, re.M|re.I)
#                 matches = pattern.findall(show_run)
#                 if not matches:
#                     df["Clasificacion"].append(categoria)
#                     df["Descripcion"].append(description)
#                     df["Impacto"].append(bp_list[categoria]["impacto"])
#                     df["Workarround"].append("Es recomendado configurar "+description+" en todos los equipos")
#                     df["Evidencia"].append(" ")
#                 else:
#                     pass
                    # df["Clasificacion"].append(categoria)
                    # df["Descripcion"].append(description)
                    # df["Impacto"].append(bp_list[categoria]["impacto"])
                    # df["Evidencia"].append(matches[0])


# dataframe = pd.DataFrame(df)
# print(dataframe)

# pattern = re.compile(r"banner\slogin", re.M|re.I)
# matches = pattern.findall(show_run)

# print(matches)

# bp_test = {
#     "Banners":
#             {
#             "Banner Message of the day (MOTD)": [r"banner\smotd", True, "bajo", "corto"],
#             "Banner Login": [r"banner\slogin",True, "bajo", "corto"],
#             "Banner Exec": [r"banner\sexec",True, "bajo", "corto"]
#             }
# }

bp_test = {
    "Banners":
            [
            ("Banner Message of the day (MOTD)", r"banner\smotd", True, "bajo", "corto"),
            ("Banner Login", r"banner\slogin" ,True, "bajo", "corto"),
            ("Banner Exec", r"banner\sexec",True, "bajo", "corto")
            ]      
}

with open("/Users/georgesolorzano/Google Drive/PythonCode/Assessment/Salcobrand/cisco_ios/RTR_ANGAMOS01/show_run.log") as file:
    show_run = file.read()

df = {
    "Clasificacion": [],
    "Descripcion": [],
    "Impacto": [],
    "Workarround": [],
    "Evidencia": []
}

for clasificacion in bp_test.keys():
    print(clasificacion)
    for bp, regex, should_match, impact, deadline in bp_test[clasificacion]:
        print(bp)
