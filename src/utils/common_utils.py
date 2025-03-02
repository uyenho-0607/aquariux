import random
import re


def string_to_number(string):
    res = string
    if isinstance(string, str):
        res = float(string.replace("$", "").replace(",", ""))
    return res


def number_to_string(number, add_units=False):
    res = number
    if isinstance(number, float) or isinstance(number, int):
        format_str = ["{:,.1f}", "${:,.1f}"][add_units]
        res = format_str.format(number)
    return res


def extract_number(text):
    match = re.search(r"\((\d+)\)", text)
    return int(match.group(1)) if match else None


def calculate_sl_tp(buy_price, sl_percentage=1, tp_percentage=3, is_selling=False):
    buy_price = string_to_number(buy_price)

    stop_loss = round(buy_price - (buy_price * sl_percentage / 100))
    take_profit = round(buy_price + (buy_price * tp_percentage / 100))

    return (take_profit, stop_loss) if is_selling else (stop_loss, take_profit)


def generate_limit_price(buy_price, is_selling=False):
    buy_price = string_to_number(buy_price)

    if is_selling:
        return round(buy_price * (1 + random.uniform(0.001, 0.005)))  # 0.1% - 0.5% higher
    return round(buy_price * (1 - random.uniform(0.001, 0.005)))  # 0.1% - 0.5% lower


def generate_stop_price(buy_price, is_selling=False):
    buy_price = string_to_number(buy_price)
    if is_selling:
        return round(buy_price * (1 - random.uniform(0.001, 0.005)))
    return round(buy_price * (1 + random.uniform(0.001, 0.005)))
