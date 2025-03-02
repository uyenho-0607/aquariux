from playwright.sync_api import expect

from src.data.enums import AssetTabs
from src.pages_object.base_page import BasePage
from src.pages_object.trade_page import TradePage
from src.utils.common_utils import number_to_string


class Notifications(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.__trade_page = TradePage(page)

        self.__notification = self.page.get_by_test_id("notification-selector")
        self.__notification_result = self.page.get_by_test_id("notification-dropdown-result")
        self.__notification_title = self.page.get_by_test_id("notification-title").last
        self.__notification_des = self.page.get_by_test_id("notification-description").last
        self.__notification_list = self.page.get_by_test_id("notification-list-result")
        self.__notification_list_items = self.__notification_list.get_by_test_id("notification-list-result-item").all()
        self.__notification_latest_item = self.__notification_list.get_by_test_id("notification-list-result-item").first

    def toggle_notification(self, close=False):
        is_open = self.__notification_result.is_visible(timeout=3000)

        if (not close and not is_open) or (close and is_open):
            self.__notification.click()

    # verify

    def verify_market_order_placed(self, order_name, size, sl, tp, is_selling=False):
        expect(self.__notification_title).to_have_text("Market Order Submitted")
        expect(self.__notification_des).to_have_text(
            f"{order_name} - {'SELL' if is_selling else 'BUY'} ORDER placed, "
            f"Size: {size} / Units: {size}. Stop Loss: {number_to_string(sl)}. Take Profit: {number_to_string(tp)}."
        )

    def verify_limit_order_placed(self, order_name, size, limit_price, sl, tp, is_sell=False):

        expect(self.__notification_title).to_have_text("Limit Order Submitted")
        expect(self.__notification_des).to_have_text(
            f"{order_name} - {'SELL' if is_sell else 'BUY'} LIMIT ORDER placed, "
            f"Size: {size} / Units: {size}. Price: {number_to_string(limit_price)}. "
            f"Stop Loss: {number_to_string(sl)}. Take Profit: {number_to_string(tp)}."
        )

    def verify_stop_order_placed(self, order_name, size, stop_price, sl, tp, is_sell=False):

        expect(self.__notification_title).to_have_text("Stop Order Submitted")
        expect(self.__notification_des).to_have_text(
            f"{order_name} - {'SELL' if is_sell else 'BUY'} STOP ORDER placed, "
            f"Size: {size} / Units: {size}. Price: {number_to_string(stop_price)}. "
            f"Stop Loss: {number_to_string(sl)}. Take Profit: {number_to_string(tp)}."
        )

    def verify_open_positions_details(self, ord_name):
        details = self.__trade_page.get_latest_asset_item_details(AssetTabs.OPEN_POSITIONS.value)

        expect(self.__notification_latest_item).to_have_text(
            f"Open Position: #{details['order_id']} {ord_name}: "
            f"Size {details['volume']} / Units {details['volume']} @ {details['entry_price']}"
        )

    def verify_closed_position_details(self, ord_name, order_id, size):
        expect(self.__notification_latest_item).to_contain_text(
            f"Position Closed: #{order_id}  {ord_name}: Size {size} / Units {size}"
        )

    def verify_order_closed(self, ord_name, is_selling=False):
        expect(self.__notification_title).to_have_text("Close Order")
        expect(self.__notification_des).to_have_text(
            f"{ord_name} - {'Sell' if is_selling else 'Buy'} order closed successfully."
        )

    def verify_market_order_updated(self, ord_name, entry_price, sl, tp, size=1, is_selling=False):
        expect(self.__notification_title).to_have_text("Market Order Updated")
        expect(self.__notification_des).to_have_text(
            f"{ord_name} - {'SELL' if is_selling else 'BUY'} ORDER updated, "
            f"Size: {size} / Units: {size}. Entry Price: {number_to_string(entry_price)}. "
            f"Stop Loss: {number_to_string(sl)}. Take Profit: {number_to_string(tp)}."
        )

    def verify_limit_order_updated(self, ord_name, limit_price, sl, tp, size=1, is_selling=False):
        expect(self.__notification_title).to_have_text("Limit Order Updated")

        expect(self.__notification_des).to_have_text(
            f"{ord_name} - {'SELL' if is_selling else 'BUY'} LIMIT ORDER updated, Size: {size} / Units: {size}. "
            f"Price: {number_to_string(limit_price)}. "
            f"Stop Loss: {number_to_string(sl)}. Take Profit: {number_to_string(tp)}."
        )

    def verify_bulk_closure(self, ord_id_list):
        expect(self.__notification_title).to_have_text("Bulk closure of open positions")

        order_ids = ", ".join(f"#{str(item)}" for item in ord_id_list[:3])

        expect(self.__notification_des).to_have_text(
            f"Positions {order_ids}"
            f"{f' and {len(ord_id_list) - 3} others' if len(ord_id_list) > 3 else ' '} have been closed."
        )

    def verify_bulk_deletion(self, ord_id_list):
        expect(self.__notification_title).to_have_text("Bulk deletion of pending orders")

        order_ids = ", ".join(f"#{str(item)}" for item in ord_id_list[:3])

        expect(self.__notification_des).to_have_text(
            f"Pending orders {order_ids}"
            f"{f' and {len(ord_id_list) - 3} others' if len(ord_id_list) > 3 else ' '} have been deleted."
        )
