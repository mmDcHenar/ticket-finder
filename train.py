from httpx import get
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
            if "Error" in data and data["ErrorType"] == "GetAvailableError":
                print(data["Error"])
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
        except Exception as e:
            send_message(str(e))
            print(e)
        sleep(1)
    sleep(30)


