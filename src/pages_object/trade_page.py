import time

from playwright.sync_api import Page, expect

from src.components.popups import Popups
from src.data.enums import OrderTypes, ExpiryTypes, AssetTabs
from src.pages_object.base_page import BasePage
from src.utils import common_utils
from src.utils.common_utils import number_to_string
from src.utils.logging_utils import logger


class TradePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.__popup = Popups(page)

        self.__all_watchlist = self.page.get_by_test_id("tab-all")
        # trade panel
        self.__one_click_toggle_checked = self.page.get_by_test_id("toggle-oct-checked")
        self.__one_click_toggle = self.page.get_by_test_id("toggle-oct")
        self.__buy_btn = self.page.get_by_test_id("trade-live-buy-price")
        self.__sell_btn = self.page.get_by_test_id("trade-live-sell-price")
        self.__order_type_dropdown = self.page.get_by_test_id("trade-dropdown-order-type")
        self.__expiry_dropdown = self.page.get_by_test_id("trade-dropdown-expiry")

        self.__trade_input_price = self.page.get_by_test_id("trade-input-price")
        self.__input_unit = self.page.get_by_test_id("trade-input-volume")
        self.__input_sl = self.page.get_by_test_id("trade-input-stoploss-price")
        self.__input_tp = self.page.get_by_test_id("trade-input-takeprofit-price")
        self.__place_order_btn = self.page.get_by_test_id("trade-button-order")

        self.__bulk_close = self.page.get_by_test_id("bulk-close")
        self.__bulk_close_all = self.page.get_by_test_id("dropdown-bulk-close-all")
        self.__bulk_delete = self.page.get_by_test_id("bulk-delete")
        self.__empty_message = self.page.get_by_test_id("empty-message")

    def __watchlist_item(self, name):
        return self.page.get_by_test_id("watchlist-symbol").get_by_text(name)

    def __order_type_options(self, option):
        return self.page.get_by_test_id(f"trade-dropdown-order-type-{option.lower()}")

    def __expiry_type_options(self, option):
        return self.page.get_by_test_id(f"trade-dropdown-expiry-good-till-{option.lower()}")

    def __asset_tab(self, option: AssetTabs):
        option = "-".join(item.lower() for item in option.split(" "))
        return self.page.get_by_test_id(f"tab-asset-order-type-{option}")

    def __asset_list(self, option: AssetTabs):
        option = option.split(" ")[0].lower()
        return self.page.get_by_test_id(f"asset-{option}-list")

    def __asset_items(self, option: AssetTabs):
        option = option.split(" ")[0].lower()
        return self.page.get_by_test_id(f"asset-{option}-list-item")

    def __asset_latest_item(self, option: AssetTabs):
        return self.__asset_items(option).first

    def __asset_latest_edit_btn(self, option: AssetTabs):
        option = option.split(" ")[0].lower()
        return self.page.get_by_test_id(f"asset-{option}-button-edit").first

    def __asset_column_value(self, option: AssetTabs, value):
        # available values: 
        # ["order-id", "order-type", "volume", "units", "entry-price", "take-profit", "stop-loss", "profit"]
        option = option.split(" ")[0].lower()
        return self.__asset_latest_item(option).get_by_test_id(f"asset-{option}-column-{value}")

    # actions
    def select_watchlist_all(self):
        self.__all_watchlist.click()

    def select_watchlist_item(self, name):
        self.__watchlist_item(name).click()

    def __select_order_type(self, option: OrderTypes):
        self.__order_type_dropdown.click()
        self.__order_type_options(option).click()

    def __select_expiry_type(self, expiry_type: ExpiryTypes):
        self.__expiry_dropdown.click()
        self.__expiry_type_options(expiry_type.rsplit(" ", 1)[-1]).click()
        return self

    def select_pending_orders_tab(self):
        self.__asset_tab(AssetTabs.PENDING_ORDERS.value).click()

    def select_order_history_tab(self):
        self.__asset_tab(AssetTabs.ORDER_HISTORY.value).click()

    def disable_one_click_trading(self):
        if self.__one_click_toggle.is_visible(timeout=5000):
            return
        self.__one_click_toggle_checked.click()

    def input_units(self, value=1):
        self.__input_unit.fill(str(value))
        return self

    def input_stop_loss(self, value):
        self.__input_sl.fill(str(value))
        return self

    def input_take_profit(self, value):
        self.__input_tp.fill(str(value))
        return self

    def input_trade_price(self, value):
        self.__trade_input_price.fill(str(value))
        return self

    def __place_buy_or_sell_order(
            self, order_type: OrderTypes, sl, tp, units=1, expiry_type=None, trade_price=None, is_selling=False,
    ):

        self.__sell_btn.click() if is_selling else self.__buy_btn.click()
        self.__select_order_type(order_type)

        if expiry_type:
            self.__select_expiry_type(expiry_type).input_trade_price(trade_price)

        self.input_units(units).input_stop_loss(sl).input_take_profit(tp).__place_order_btn.click()
        self.__popup.confirm_trade()

    def place_buy_order(
            self, order_type: OrderTypes, sl, tp, units=1, expiry_type=None, trade_price=None
    ):
        self.__place_buy_or_sell_order(order_type, sl, tp, units, expiry_type=expiry_type, trade_price=trade_price)

    def place_sell_order(
            self, order_type: OrderTypes, sl, tp, units=1, expiry_type=None, trade_price=None
    ):
        self.__place_buy_or_sell_order(order_type, sl, tp, units, expiry_type, trade_price, is_selling=True)

    def get_asset_order_id_list(self, option: AssetTabs):
        res = [
            item.get_by_test_id(f"asset-{option.split(' ')[0].lower()}-column-order-id").text_content()
            for item in self.__asset_items(option).all()
        ]
        return res

    def get_asset_tab_amount(self, option: AssetTabs):
        return common_utils.extract_number(self.__asset_tab(option).text_content())

    def get_latest_asset_item_details(self, option: AssetTabs):
        keys = ["order_id", "order_type", "volume", "units", "entry_price", "take_profit", "stop_loss", "profit"]
        return {
            k: self.__asset_column_value(option, '-'.join(k.split('_'))).text_content() for k in keys
        }

    def get_buy_price(self):
        return self.__buy_btn.text_content()

    def get_sell_price(self):
        return self.__sell_btn.text_content()

    # open position
    def bulk_close_all_open_positions(self):
        self.__bulk_close.click()
        self.__bulk_close_all.click()
        self.__popup.confirm_bulk_close()

    def close_open_position(self):
        locator = self.__asset_latest_item(AssetTabs.OPEN_POSITIONS.value)
        locator.get_by_test_id("asset-open-button-close").click()
        self.__popup.confirm_close_order()

    def update_open_position(self, sl, tp):
        logger.info(f"- update with sl: {sl!r}, tp: {tp!r}")
        self.__asset_latest_edit_btn(AssetTabs.OPEN_POSITIONS.value).click()
        time.sleep(0.5)  # wait a bit for more stable
        self.__popup.input_edit_sl(sl).input_edit_tp(tp).update_order().confirm_update_order()

    # pending orders
    def update_pending_order(self, limit_price, sl, tp, expiry_type):
        self.__asset_latest_edit_btn(AssetTabs.PENDING_ORDERS.value).click()
        time.sleep(0.5)  # wait a bit for more stable
        (self.__popup.input_edit_price(limit_price)
         .input_edit_sl(sl).input_edit_tp(tp).edit_expiry(expiry_type).update_order().confirm_update_order())

    def bulk_delete_pending_orders(self):
        self.select_pending_orders_tab()
        self.__bulk_delete.click()
        self.__popup.confirm_bulk_delete()

    # verify

    def verify_asset_tab_amount(self, option: AssetTabs, exp_amount):
        expect(self.__asset_tab(option)).to_contain_text(f"({str(exp_amount)})")

    def __verify_latest_asset_item_details(
            self, option: AssetTabs, size, tp, sl, expiry_type=None, trade_price=None, is_stop=False,
            is_sell=False, ):

        logger.info("- Check order_type")
        order_type = ['BUY', 'SELL'][is_sell]
        if option != AssetTabs.OPEN_POSITIONS.value:
            order_type += f" {['LIMIT', 'STOP'][is_stop]}"

        expect(self.__asset_column_value(option, 'order-type')).to_have_text(order_type)

        logger.info("- Check size & units")
        expect(self.__asset_column_value(option, 'volume')).to_have_text(str(size))
        expect(self.__asset_column_value(option, 'units')).to_have_text(str(size))

        logger.info("- Check take profit")
        expect(self.__asset_column_value(option, 'take-profit')).to_have_text(number_to_string(tp))

        logger.info("- Check stop loss")
        expect(self.__asset_column_value(option, 'stop-loss')).to_have_text(number_to_string(sl))

        if expiry_type:
            logger.info("- Check expiry type")
            expect(self.__asset_column_value(option, 'expiry')).to_have_text(expiry_type)

        if trade_price:
            logger.info("- Check entry price")
            expect(self.__asset_column_value(option, 'entry-price')).to_have_text(number_to_string(trade_price))

    def verify_latest_open_position_details(self, size, tp, sl, is_sell=False):
        self.__verify_latest_asset_item_details(AssetTabs.OPEN_POSITIONS.value, size, tp, sl, is_sell=is_sell)

    def verify_latest_pending_order_details(self, size, tp, sl, expiry_type, trade_price, is_sell=False, is_stop=False):
        self.__verify_latest_asset_item_details(
            AssetTabs.PENDING_ORDERS.value, size, tp, sl, expiry_type, trade_price, is_stop, is_sell=is_sell)

    def verify_latest_order_history_details(self, status, size, entry_price, tp, sl, is_stop=False, is_sell=False):
        self.select_order_history_tab()
        option = AssetTabs.ORDER_HISTORY.value
        self.__verify_latest_asset_item_details(option, size, tp, sl, entry_price, is_stop=is_stop, is_sell=is_sell)

        logger.info("- Check status")
        expect(self.__asset_column_value(option, 'status')).to_have_text(status)

    def verify_open_position_not_displayed(self, ord_id):
        # expect(
        #     self.__asset_list(AssetOrderOptions.OPEN_POSITIONS.value)
        #     .get_by_test_id("asset-open-list-item")
        #     .get_by_test_id("asset-open-column-order-id").get_by_text(str(ord_id))
        # ).not_to_be_visible()

        expect(
            self.__asset_items(AssetTabs.OPEN_POSITIONS.value)
            .get_by_test_id("asset-open-column-order-id").get_by_text(str(ord_id))
        ).not_to_be_visible()

    def verify_amount_asset_items_displaying(self, option, exp_amount):
        expect(self.__asset_items(option)).to_have_count(exp_amount)

    def verify_no_open_positions_message(self, order_name):
        expect(self.__empty_message).to_have_text(f"No open positions for {order_name}")

    def verify_no_pending_orders_message(self, order_name):
        expect(self.__empty_message).to_have_text(f"No pending orders for {order_name}")
