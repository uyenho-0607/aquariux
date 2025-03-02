from src.data.enums import ExpiryTypes
from src.pages_object.base_page import BasePage
from src.utils.common_utils import string_to_number


class Popups(BasePage):
    def __init__(self, page):
        super().__init__(page)

        self.__trade_confirm = self.page.get_by_test_id("trade-confirmation-button-confirm")
        self.__close_order_confirm = self.page.get_by_test_id("close-order-button-submit")
        self.__update_order = self.page.get_by_test_id("edit-button-order")

        self.__edit_sl_price = self.page.get_by_test_id("edit-input-stoploss-price")
        self.__edit_tp_price = self.page.get_by_test_id("edit-input-takeprofit-price")

        self.__edit_price = self.page.get_by_test_id("edit-input-price")
        self.__edit_expiry_dropdown = self.page.get_by_test_id("edit-dropdown-expiry")
        self.__edit_expiry_cancelled = self.page.get_by_test_id("edit-dropdown-expiry-good-till-cancelled")
        self.__edit_expiry_day = self.page.get_by_test_id("edit-dropdown-expiry-good-till-day")

        self.__update_order_confirm = self.page.get_by_test_id("edit-confirmation-button-confirm")
        self.__bulk_close_confirm = self.page.get_by_test_id("bulk-close-modal-button-submit-all")
        self.__bulk_delete_confirm = self.page.get_by_test_id("bulk-delete-modal-button-submit")

    def confirm_trade(self):
        self.__trade_confirm.click()

    def confirm_bulk_delete(self):
        self.__bulk_delete_confirm.click()

    def confirm_close_order(self):
        self.__close_order_confirm.click()

    def update_order(self):
        self.__update_order.click()
        return self

    def input_edit_sl(self, value):
        value = string_to_number(value)
        self.__edit_sl_price.fill(str(value))
        return self

    def input_edit_tp(self, value):
        value = string_to_number(value)
        self.__edit_tp_price.fill(str(value))
        return self

    def input_edit_price(self, value):
        value = string_to_number(value)
        self.__edit_price.fill(str(value))
        return self

    def edit_expiry(self, expiry_type):
        self.__edit_expiry_dropdown.click()
        match expiry_type:
            case ExpiryTypes.CANCELLED.value:
                self.__edit_expiry_cancelled.click()

            case _:
                self.__edit_expiry_day.click()
        return self

    def confirm_update_order(self):
        self.__update_order_confirm.click()

    def confirm_bulk_close(self):
        self.__bulk_close_confirm.click()
