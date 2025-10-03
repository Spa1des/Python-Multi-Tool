import os
import base64
import requests
import socket
import json
import time
import ipaddress
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from datetime import datetime
import pyfiglet

logo = """
                                 ████████╗ ██████╗  ██████╗ ██╗     
                                 ╚══██╔══╝██╔═══██╗██╔═══██╗██║     
                                    ██║   ██║   ██║██║   ██║██║     
                                    ██║   ██║   ██║██║   ██║██║     
                                    ██║   ╚██████╔╝╚██████╔╝███████╗
                                    ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝                                   
"""

menu = """
                                     1.Ping
                                     2.IP Config
                                     3.Encode
                                     4.Decode
                                     5.Webhook Message
                                     6.SSH
                                     7.Trace Route
                                     8.Port Scan
                                     9.IP Geo
"""

def clear():
    os.system("cls")

def ping():
    clear()
    host = input("Enter an IP or Web URL: ")
    os.system(f"ping {host}")
    
def ipconfig():
    clear()
    os.system("ipconfig")

def encode():
    clear()
    encode_text = input("Text to encode: ")
    encoded_bytes = base64.b64encode(encode_text.encode("utf-8"))
    encoded_str = encoded_bytes.decode("utf-8")
    print("\nEncoded text:", encoded_str)

def decode():
    clear()
    decode_text = input("Text to decode: ")
    try:
        decoded_bytes = base64.b64decode(decode_text.encode("utf-8"))
        decoded_str = decoded_bytes.decode("utf-8")
        print("\nDecoded text:", decoded_str)
    except Exception as e:
        print("\nError decoding:", e)
  
def webhookmsg():
    clear()
    webhook = input("Enter a webhook URL: ")
    message = input("Enter your message: ")
    
    response = requests.post(webhook, json={"content": message})
    
    if response.status_code == 204:
        print("Message sent...")
    else:
        print(f"Failed to send message...")

def ssh():
    clear()
    hostname = input("Enter a Hostname: ")
    port = input("Enter a Port: ")
    os.system(f"ssh -p {port} {hostname}")

def tracert():
    clear()
    host = input("Enter an IP or Hostname: ")
    output = os.system(f"tracert {host}")
    print(output)
    
def portscan():
    clear()
    common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 3389, 8080]
    host = input("Enter an IP or Hostname: ")
    for port in common_ports:
        s = socket.socket()
        s.settimeout(0.2)
        try:
            s.connect((host, port))
            print(f"Port {port} OPEN")
        except Exception:
            pass
        finally:
            s.close()

def ipgeo():
    clear()
    target = input("Enter IP or hostname: ").strip()
    if not target:
        return

    clear()

    try:
        ipaddress.ip_address(target)
        resolved = target
    except ValueError:
        try:
            infos = socket.getaddrinfo(target, None, family=socket.AF_INET)
            resolved = infos[0][4][0] if infos else target
        except socket.gaierror:
            resolved = target

    try:
        ip = ipaddress.ip_address(resolved)
        if ip.version == 4 and (ip.is_private or ip.is_loopback or ip.is_link_local):
            print(f"[ERROR] {target} is a private IPv4 ({resolved})")
            print("-"*40)
            return
    except ValueError:
        pass

    api_url = f"http://ip-api.com/json/{resolved}?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,query"
    try:
        req = Request(api_url, headers={"User-Agent": "ip-geo/simple"})
        with urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
    except (HTTPError, URLError) as e:
        data = {"status": "fail", "message": str(e), "query": resolved}

    if data.get("status") != "success":
        print(f"[ERROR] {data.get('query')}: {data.get('message')}")
    else:
        for k in ("country","countryCode","region","regionName","city","zip","lat","lon","timezone","isp","org","query"):
            print(f"{k.capitalize():<12}: {data.get(k,'—')}")
    print("-"*40)
    
def main():
    while True:
        clear()
        print(logo)
        print(menu)
        choice = input("Choose an option (q to quit): ")

        if choice == "1":
            ping()
            input("\nPress Enter to return to menu...")
        elif choice == "2":
            ipconfig()
            input("\nPress Enter to return to menu...")
        elif choice == "3":
            encode()
            input("\nPress Enter to return to menu...")
        elif choice == "4":
            decode()
            input("\nPress Enter to return to menu...")
        elif choice == "5":
            webhookmsg()
            input("\nPress Enter to return to menu...")
        elif choice == "6":
            ssh()
            input("\nPress Enter to return to menu...")
        elif choice == "7":
            tracert()
            input("\nPress Enter to return to menu...")
        elif choice == "8":
            portscan()
            input("\nPress Enter to return to menu...")
        elif choice == "9":
            ipgeo()
            input("\nPress Enter to return to menu...")
        elif choice.lower() == "q":
            break
        else:
            print("Invalid choice.")
            input("\nPress Enter to try again...")
            
main()
