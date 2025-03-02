import random

import pytest

from src.data.enums import AssetTabs, OrderTypes, ExpiryTypes
from src.utils.common_utils import generate_limit_price
from src.utils.logging_utils import logger


def test(pages, order_name, test_setup):
    ord_id_list = pages.trade_page.get_asset_order_id_list(AssetTabs.PENDING_ORDERS.value)

    logger.info(f"Step: Bulk delete pending orders")
    pages.trade_page.bulk_delete_pending_orders()

    logger.info("Verify bulk deletion notification")
    pages.home_page.notifications.verify_bulk_deletion(ord_id_list)

    logger.info("Verify empty message in pending orders tab")
    pages.trade_page.verify_no_pending_orders_message(order_name)

    logger.info("Verify NO pending orders is displaying")
    pages.trade_page.verify_amount_asset_items_displaying(AssetTabs.PENDING_ORDERS.value, 0)

    logger.info("Verify amount of pending orders tab is 0")
    pages.trade_page.verify_asset_tab_amount(AssetTabs.PENDING_ORDERS.value, 0)


@pytest.fixture
def test_setup(place_orders, pages):
    place_orders(
        order_amount=random.randint(1, 4),
        order_type=OrderTypes.LIMIT.value,
        expiry_type=random.choice(list(ExpiryTypes)).value,
        trade_price=generate_limit_price(pages.trade_page.get_buy_price())
    )
    pages.trade_page.select_pending_orders_tab()
