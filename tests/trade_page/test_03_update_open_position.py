import random

from src.data.enums import AssetTabs
from src.utils import common_utils
from src.utils.logging_utils import logger


def test(pages, order_name, place_orders):

    is_selling = random.randint(0, 1)
    place_orders(is_selling=is_selling)

    sl, tp = common_utils.calculate_sl_tp(pages.trade_page.get_buy_price(), 2, 5, is_selling)
    entry_price = pages.trade_page.get_latest_asset_item_details(AssetTabs.OPEN_POSITIONS.value)['entry_price']

    logger.info(f"Step: Edit first item in open position list")
    pages.trade_page.update_open_position(sl, tp)

    logger.info("Verify order updated notification")
    pages.home_page.notifications.verify_market_order_updated(order_name, entry_price, sl, tp, is_selling=is_selling)

    logger.info("Verify open position details is updated")
    pages.trade_page.verify_latest_open_position_details(1, tp, sl, is_sell=is_selling)
