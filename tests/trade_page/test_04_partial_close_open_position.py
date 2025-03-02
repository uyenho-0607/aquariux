import random

import pytest

from src.data.enums import AssetTabs
from src.utils.logging_utils import logger


def test(pages, order_name, test_setup):
    is_selling = test_setup
    asset_tab = AssetTabs.OPEN_POSITIONS.value

    cur_amount = pages.trade_page.get_asset_tab_amount(asset_tab)
    position_details = pages.trade_page.get_latest_asset_item_details(asset_tab)

    logger.info(f"Step: Close first open position")
    pages.trade_page.close_open_position()

    logger.info("Verify closed position notification")
    pages.home_page.notifications.verify_order_closed(order_name, is_selling=is_selling)

    logger.info(f"Verify {cur_amount - 1} of open position displaying")
    pages.trade_page.verify_amount_asset_items_displaying(asset_tab, cur_amount - 1)

    logger.info(f"Verify open position tab amount is {cur_amount - 1}")
    pages.trade_page.verify_asset_tab_amount(asset_tab, cur_amount - 1)

    logger.info(f"Verify open position #{position_details['order_id']} is no longer displayed")
    pages.trade_page.verify_open_position_not_displayed(position_details['order_id'])

    logger.info("Verify closed position notifications details")
    pages.home_page.notifications.toggle_notification()
    pages.home_page.notifications.verify_closed_position_details(
        order_name, position_details['order_id'], position_details['volume'])


@pytest.fixture
def test_setup(place_orders, pages):
    is_selling = random.randint(0, 1)
    place_orders(is_selling=is_selling)
    yield is_selling
    pages.home_page.notifications.toggle_notification(close=True)
