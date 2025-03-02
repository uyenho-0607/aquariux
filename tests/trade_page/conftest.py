import pytest

from src.data.enums import OrderTypes, AssetTabs
from src.utils.common_utils import calculate_sl_tp
from src.utils.logging_utils import logger


@pytest.fixture(scope="package", autouse=True)
def setup(pages, order_name):
    logger.info("- Open Trade page")
    pages.home_page.open_trade_page()

    logger.info("- Select watch list all tab")
    # time.sleep(1)
    pages.trade_page.select_watchlist_all()

    logger.info("- Select watch list item")
    pages.trade_page.select_watchlist_item(order_name)
    # time.sleep(2)

    logger.info("- Disable one click trading")
    pages.trade_page.disable_one_click_trading()


@pytest.fixture(scope="package")
def order_name():
    return "BTCUSD.std"


@pytest.fixture
def place_orders(pages):
    def _handler(order_amount=1, order_type=OrderTypes.MARKET.value, is_selling=False, **kwargs):
        asset_tab = [AssetTabs.PENDING_ORDERS, AssetTabs.OPEN_POSITIONS][order_type == OrderTypes.MARKET.value]
        cur_amount = pages.trade_page.get_asset_tab_amount(asset_tab.value)

        logger.info(f"- Make {order_amount} {order_type!r} order(s)")

        sl, tp = calculate_sl_tp(pages.trade_page.get_buy_price(), is_selling=is_selling)

        place_order_func = pages.trade_page.place_sell_order if is_selling else pages.trade_page.place_buy_order
        for _ in range(order_amount):
            place_order_func(order_type, sl, tp, **kwargs)

        pages.trade_page.verify_asset_tab_amount(asset_tab.value, cur_amount + order_amount)

    return _handler
