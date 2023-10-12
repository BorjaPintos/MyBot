from datetime import datetime
import requests


class CheckURLUseCase:

    def __init__(self):
        pass

    def check_url(self, url: str) -> dict:
        info_response = {
            "url": url,
            "timestamp": datetime.now().strftime("%d-%m-%Y - %H:%M:%S")}
        try:
            response = requests.get(url)
            info_response["status_code"] = response.status_code
            info_response["content_length"] = len(response.text)
        except Exception as e:
            info_response["error"] = str(e)

        return info_response
