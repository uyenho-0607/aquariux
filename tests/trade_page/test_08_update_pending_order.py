import random

import pytest

from src.data.enums import ExpiryTypes, OrderTypes
from src.utils.common_utils import generate_limit_price, calculate_sl_tp
from src.utils.logging_utils import logger


def test(pages, order_name, test_setup):

    expiry_type = random.choice(list(ExpiryTypes)).value
    limit_price = generate_limit_price(pages.trade_page.get_buy_price())
    sl, tp = calculate_sl_tp(limit_price)

    logger.info(f"Step: Edit first item in open position list")
    pages.trade_page.update_pending_order(limit_price, sl, tp, expiry_type)

    logger.info("Verify order updated notification")
    pages.home_page.notifications.verify_limit_order_updated(order_name, limit_price, sl, tp)

    logger.info("Verify pending order details updated")
    pages.trade_page.verify_latest_pending_order_details(1, tp, sl, expiry_type, limit_price)


@pytest.fixture
def test_setup(place_orders, pages):
    place_orders(
        order_type=random.choice([OrderTypes.STOP, OrderTypes.LIMIT]).value,
        expiry_type=random.choice(list(ExpiryTypes)).value,
        trade_price=generate_limit_price(pages.trade_page.get_buy_price())
    )
    pages.trade_page.select_pending_orders_tab()
