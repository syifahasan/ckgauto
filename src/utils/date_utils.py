from datetime import datetime


def today_title() -> str:
    return datetime.today().strftime("%Y-%m-%d")
