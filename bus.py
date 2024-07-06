from httpx import get
from time import sleep

from json import dumps

url = "https://safar724.com/bus/getservices?origin=11320000&destination=26310000&date=1402-12-03"
bot_token = "TOKEN"
chat_id = 123456789

telegram_api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

text = """\
Company: *{company}*
Time: *{time}*
Available seats: `{seats}`
Price: `{price:,}`
"""

def send_message(text: str) -> None:
    get(telegram_api_url, params={"chat_id": chat_id, "text": text, "parse_mode": "markdown"})

temp = {}
while True:
    try:
        data = get(url).json()
        for item in data["Items"]:
            if item["AvailableSeatCount"]:
                if item["ID"] not in temp or temp[item["ID"]] != item["AvailableSeatCount"]:
                    message = text.format(
                        company=item["CompanyPersianName"],
                        time=item["DepartureTime"],
                        seats=item["AvailableSeatCount"],
                        price=item["Price"]
                    )
                    send_message(message)
                    temp[item["ID"]] = item["AvailableSeatCount"]
    except Exception as e:
        send_message(str(e))
    print(temp)
    sleep(30)


