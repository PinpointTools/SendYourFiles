import requests
import os

# main reason why this is here:
# 1. catbox for some reason need this
# 2. this is probably required
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Origin": "https://catbox.moe",
    "Referer": "https://catbox.moe/",
}

def catbox(file_path):
    url = "https://catbox.moe/user/api.php"
    try:
        with open(file_path, "rb") as f:
            files = {"fileToUpload": (os.path.basename(file_path), f)}
            data = {"reqtype": "fileupload"}
            response = requests.post(url, data=data, files=files, headers=HEADERS)

            if response.status_code == 200:
                result = response.text.strip()
                if result:
                    return result
                return "Error: Server returned empty response."
            return f"Server Error: {response.status_code}"
    except Exception as e:
        return f"Request Failed: {str(e)}"


def litterbox(file_path, duration="1h"):
    url = "https://litterbox.catbox.moe/resources/internals/api.php"
    try:
        with open(file_path, "rb") as f:
            files = {"fileToUpload": (os.path.basename(file_path), f)}
            data = {"reqtype": "fileupload", "time": duration}
            response = requests.post(url, data=data, files=files, headers=HEADERS)

            if response.status_code == 200:
                result = response.text.strip()
                if result:
                    return result
                return "Error: Server returned empty response."
            return f"Server Error: {response.status_code}"
    except Exception as e:
        return f"Request Failed: {str(e)}"


def buzzheavier(file_path):
    filename = os.path.basename(file_path)
    url = f"https://w.buzzheavier.com/{filename}"
    try:
        with open(file_path, "rb") as f:
            response = requests.put(url, data=f, headers=HEADERS)
            if response.status_code in [200, 201]:
                data = response.json()
                fileID = data.get("data", {}).get("id")
                if fileID:
                    return f"https://buzzheavier.com/{fileID}"
                return "Error: Could not find file ID in response."
            return f"Server Error: {response.status_code}"
    except Exception as e:
        return f"Request Failed: {str(e)}"
