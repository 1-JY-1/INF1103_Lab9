from orderline import OrderLine
from product import Product
from DiscountStrategy import DiscountStrategy, NoDiscount, PercentageDiscount, BulkDiscount, StudentDiscount

class Order:
    def __init__(self, order_id: str, discount: DiscountStrategy = None):
        self.order_id: str = order_id
        self.order_lines: list[OrderLine] = []
        self.discount = discount if discount is not None else NoDiscount()


    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)
        self.order_lines.append(order_line)


    def calculate_total(self) -> float:
        total = sum(line.calculate_subtotal() for line in self.order_lines)
        return self.discount.apply(total)


    def set_discount(self, discount: DiscountStrategy):
        self.discount = discount