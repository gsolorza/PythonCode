import re

show_run = "Building configuration...\n\nCurrent configuration : 1106 bytes\n!\nversion 15.1\nservice timestamps debug datetime msec\nservice timestamps log datetime msec\nno service password-encryption\nservice compress-config\n!\nhostname CE-A\n!\nboot-start-marker\nboot-end-marker\n!\n!\n!\nusername cisco privilege 15 secret 5 $1$t00T$Y/5i3OevQWcXx0j/shIZE1\nno aaa new-model\nclock timezone EET 2 0\n!\nip cef\n!\n!\nno ip domain-lookup\nip domain-name cisco.com\nno ipv6 cef\nipv6 multicast rpf use-bgp\n!\n!\n!\n!\n!\n!\n!\nspanning-tree mode pvst\nspanning-tree extend system-id\n!\n!\n!\n!\nvlan internal allocation policy ascending\n!\n! \n!\n!\n!\n!\n!\n!\n!\n!\ninterface Loopback0\n ip address 10.10.10.10 255.255.255.255\n ip ospf network point-to-point\n!\ninterface Ethernet0/0\n duplex auto\n!\ninterface Ethernet0/1\n no switchport\n ip address 10.2.10.10 255.255.255.0\n duplex auto\n!\ninterface Ethernet0/2\n shutdown\n duplex auto\n!\ninterface Ethernet0/3\n shutdown\n duplex auto\n!\n!\nno ip http server\n!\nip route 0.0.0.0 0.0.0.0 10.2.10.2\nip route 10.6.20.0 255.255.255.0 10.1.10.1\n!\n!\n!\n!\ncontrol-plane\n!\n!\nline con 0\n privilege level 15\n logging synchronous\nline aux 0\nline vty 0 4\n login local\n transport input ssh\n!\nend\n"

bp_list = {
    "Categorias": [
        {"Banners":
            {
                "descripcion": "Banner Best Practices",
                "impacto": "bajo",
                "plazo": "corto",
                "regex": 
                {
                    "Banner Message of the day (MOTD)": r"banner\smotd.*",
                    "Banner Login": r"banner\slogin.*",
                    "Banner Exec": r"banner\sexec.*"
                }
            
            },
        "Authentication, Authorization and Accouting":
            {
                "description": "AAA Best Practices",
                "impacto": "medio",
                "plazo": "corto",
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
                "descripcion": "Line VTY Best Practices",
                "impacto": "low",
                "plazo": "medio",
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
                "description": "Logging Best Practices",
                "impacto": "low",
                "plazo": "medio",
                "regex": 
                {
                    "Centralized Logging": r"logging host.*",
                    "Logging Buffered": r"logging buffered.*",
                    "Logging Source-Interface": r"logging source-interface\s.*"
                }
            },
        "Simple Network Management Protocol (SNMP)": 
            {
                "description": "SNMP Best Practices",
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
                "description": "Time and NTP Best Practices",            
                "impacto": "low",
                "plazo": "medio",
                "regex":  
                {
                    "Timezone Configured": r"clock timezone\s.*",
                    "NTP server Configured": r"ntp server \d+\.\d+\.\d+\.\d+(\s\w+|$|\s$)$"
                }  
            },
        "Comandos que deben ser evitados":
            {
                "description": "Commands that should be avoided",
                "impacto": "low",
                "plazo": "medio",
                "regex":
            
                {
                    "Password 7 in Line VTY": r"^\spassword\s\d\s\w*$",
                    "Password 7 or 0 for Username": r"username\s.*password\s.*",
                    "http/https Enabled": r"^ip http server",
                    "Enable Password": r"^enable password\s\w+$",
                    "Generic user names created": r"^username\scisco|username\sadmin"
                }  
            }
        }
    ]
}




matches = []

for bp in bp_list["Categorias"]:
    for categoria, bp_attributes in bp.items():
        for key, value in bp_attributes.items():

            if key == "regex":
                for description, reg in value.items():
                    pattern = re.compile(reg, re.M|re.I)
                    matches = pattern.finditer(show_run)
                    for match in matches:
                        print(match.group(0))




