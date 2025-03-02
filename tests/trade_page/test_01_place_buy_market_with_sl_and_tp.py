import pytest

from src.data.enums import OrderTypes
from src.utils.common_utils import calculate_sl_tp
from src.utils.logging_utils import logger


def test(pages, order_name, test_teardown):

    order_type = OrderTypes.MARKET.value
    sl, tp = calculate_sl_tp(pages.trade_page.get_buy_price())

    logger.info(f"Step: Make {order_type!r} order with stop loss: {sl!r} and take profit: {tp!r}")
    pages.trade_page.place_buy_order(order_type, sl, tp)

    logger.info("Verify placed order succeeded notification")
    pages.home_page.notifications.verify_market_order_placed(order_name, 1, sl, tp)

    logger.info("Verify open position details")
    pages.trade_page.verify_latest_open_position_details(1, tp, sl)

    logger.info("Verify notification details")
    pages.home_page.notifications.toggle_notification()
    pages.home_page.notifications.verify_open_positions_details(order_name)


@pytest.fixture
def test_teardown(pages):
    yield
    pages.home_page.notifications.toggle_notification(close=True)
