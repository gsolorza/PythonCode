import napalm
import json
from pprint import pprint

def main():
    driver_ios = napalm.get_network_driver("ios")
    ios_router = driver_ios(
    hostname = "10.253.8.168",
    username = "lairdadmin",
    password = "WgU0znN(qhxf"
    )
    print("Connecting to IOS Router...")
    ios_router.open()
    print("Checking IOS Router Connection Status:")
    output = ios_router.get_interfaces_ip()
    print(json.dumps(output, sort_keys=True, indent=4))
    ios_router.close()
    print("Test Completed")
if __name__ == "__main__":
    main()