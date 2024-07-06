from httpx import get, ConnectTimeout
from time import sleep

from json import dumps

url = "https://train.atighgasht.com/TrainService/api/GetAvailable/v2?from=191&to=55&date=2024-07-{day}&adultCount=1&childCount=0&infantCount=0&exclusive=false&availableStatus=Both&genderCode=3"
bot_token = "TOKEN"
chat_id = 123456789

def send_message(text: str) -> None:
    get(
        f"https://api.telegram.org/bot{bot_token}/sendMessage",
        params={
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "markdown"
            }
        )

while True:
    for i in range(13, 20):
        try:
            data = get(url.format(day=i)).json()
            print(url.format(day=i))
            if "Error" in data:
                if data["ErrorType"] == "GetAvailableError":
                    pass
                elif data["ErrorType"] == "RateLimitExceeded":
                    send_message(data["Error"])
                    sleep(10*60)
                print(data["Error"])
                break
            if "Trains" not in data:
                print(data)
                break
            for train in data["Trains"]:
                for p in train["Prices"]:
                    for c in p["Classes"]:
                        text = f"""\
    Company: *{c["WagonName"]}*
    From: *{train["FromName"]}*
    To: *{train["ToName"]}*
    Date: *{train["Weekday"]} {train["DateString"]}*
    Time: *{train["DepartureTime"][-8:-3]}*
    Available seats: `{c["Capacity"]}`
    Price: `{c["Price"]:,}`
    """
                        if c["Capacity"]:
                            send_message(text)
                            print(text)
        except ConnectTimeout as e:
            print(e)
        except Exception as e:
            print(e)
            send_message(str(e))
        sleep(2)
    sleep(120)


