import random
from enum import Enum


class SidebarOptions(Enum):
    TRADE = "Trade"
    MARKETS = "Markets"
    ASSETS = "Assets"
    SIGNAL = "Signal"
    NEWS = "News"
    EDUCATION = "Education"


# Trade Page
class WatchListTabs(Enum):
    ALL = "All"
    FAVOURITES = "Favourites"
    TOP_PICKS = "Top Picks"
    TOP_GAINER = "Top Gainer"
    TOP_LOSER = "Top Loser"


class OrderTypes(Enum):
    MARKET = "Market"
    LIMIT = "Limit"
    STOP = "Stop"


class ExpiryTypes(Enum):
    CANCELLED = "Good Till Cancelled"
    DAY = "Good Till Day"


class AssetTabs(Enum):
    OPEN_POSITIONS = "Open Positions"
    PENDING_ORDERS = "Pending Orders"
    ORDER_HISTORY = "Order History"


class OrderHistoryStatus(Enum):
    CLOSED = "Closed"
    CANCELLED = "Cancelled"


if __name__ == '__main__':
    print(random.choice(list(ExpiryTypes)))
