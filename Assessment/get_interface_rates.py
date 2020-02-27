#!/usr/bin/env python3
from pprint import pprint

def get_interface_rates(connection):
    if connection.device_type == "cisco_ios":
        output = connection.send_command("show interfaces | in line|input rate|output rate")
        output_list = output.split("\n")

        ietf_rates = {}

        interfaces = []
        input_rate = []
        output_rate = []
        interval = []
        pps_input = []
        pps_output = []

        for out in output_list:
            if "line" in out:
                interfaces.append(out.split(" ")[0])
            elif "input" in out:
                interval.append(" ".join(out.split(" ")[2:4]))
                input_rate.append(" ".join(out.split(" ")[6:7]))
                pps_input.append(" ".join(out.split(" ")[8:9]))
            elif "output" in out:
                output_rate.append(" ".join(out.split(" ")[6:7]))
                pps_output.append(" ".join(out.split(" ")[8:9]))

        result = zip(interfaces, input_rate, output_rate, interval, pps_input, pps_output)

        for ietf, irate, orate, interval, pps_input, pps_output in list(result):
            ietf_rates.update(
                { ietf: {
                "rates": {
                    "interval": interval,
                    "input-rate-bps": irate,
                    "input-rate-pps": pps_input, 
                    "output-rate-bps": orate,
                    "output-rate-pps": pps_output
                    }    
                } 
                }
                )

        return ietf_rates
    else:
        print("THE OS SPECIFIED DO NOT SUPPORT THIS FUNCTION")

def get_interface_usage(connection):
    if connection.device_type == "cisco_ios":
        output = connection.send_command("show interface status", use_textfsm=True)
        pprint(output)

    else:
        print("THE OS SPECIFIED DO NOT SUPPORT THIS FUNCTION")
