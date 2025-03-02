import random

from src.data.enums import OrderTypes, ExpiryTypes
from src.utils.common_utils import calculate_sl_tp, generate_limit_price
from src.utils.logging_utils import logger


def test(pages, order_name):

    order_type = OrderTypes.LIMIT.value
    limit_price = generate_limit_price(pages.trade_page.get_buy_price())
    sl, tp = calculate_sl_tp(limit_price)
    expiry_type = random.choice(list(ExpiryTypes)).value

    logger.info(f"Step: Make {order_type!r} order with expiry type: {expiry_type!r}")
    pages.trade_page.place_buy_order(order_type, sl, tp, 1, expiry_type, limit_price)

    logger.info("Verify placed order succeeded notification")
    pages.home_page.notifications.verify_limit_order_placed(order_name, 1, limit_price, sl, tp)

    logger.info("Verify pending orders details")
    pages.trade_page.select_pending_orders_tab()
    pages.trade_page.verify_latest_pending_order_details(1, tp, sl, expiry_type, limit_price)
