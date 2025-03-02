import random

import pytest

from src.data.enums import AssetTabs
from src.utils.logging_utils import logger


def test(pages, test_setup, order_name):

    ord_id_list = pages.trade_page.get_asset_order_id_list(AssetTabs.OPEN_POSITIONS.value)

    logger.info(f"Step: Bulk close all open positions")
    pages.trade_page.bulk_close_all_open_positions()

    logger.info("Verify bulk closure notification")
    pages.home_page.notifications.verify_bulk_closure(ord_id_list)

    logger.info("Verify empty message in open position tab")
    pages.trade_page.verify_no_open_positions_message(order_name)

    logger.info("Verify amount of open positions displaying is 0")
    pages.trade_page.verify_amount_asset_items_displaying(AssetTabs.OPEN_POSITIONS.value, 0)

    logger.info("Verify amount of open positions tab is 0")
    pages.trade_page.verify_asset_tab_amount(AssetTabs.OPEN_POSITIONS.value, 0)


@pytest.fixture
def test_setup(place_orders):
    place_orders(random.randint(1, 4), is_selling=random.randint(0, 1))
