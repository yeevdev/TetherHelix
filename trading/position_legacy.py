class Position:

    def __init__(self, entry_price, volume, created_at, order_uuid):
        self.entry_price = entry_price
        self.volume = volume
        self.order_uuid = order_uuid
        self.created_at = created_at
        self.is_open = True

    def close(self):
        self.is_open = False
