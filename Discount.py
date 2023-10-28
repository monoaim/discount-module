class Discount:
    def apply_discount(self, cart, total):
        pass


class Coupon(Discount):
    def __init__(self, discount_type, value):
        self.discount_type = discount_type
        self.value = value

    def apply_discount(self, cart, total):
        if self.discount_type == "Fixed":
            return self.value
        elif self.discount_type == "Percentage":
            return total * (self.value / 100)
        else:
            raise ValueError("Unsupported discount type for Coupon")


class OnTop(Discount):
    def __init__(self, discount_type, category, value):
        self.discount_type = discount_type
        self.category = category
        self.value = value

    def apply_discount(self, cart, total):
        if self.discount_type == "PercentageByItemCategory":
            category_total = sum(item['price'] * item['quantity'] for item in cart if item['category'] == self.category)
            return category_total * (self.value / 100)
        elif self.discount_type == "DiscountByPoints":
            # 1 Point = 1 THB and capping at 20% of total price
            discount_value = min(self.value, total * 0.20)
            return discount_value
        else:
            raise ValueError("Unsupported discount type for OnTop")


class Seasonal(Discount):
    def __init__(self, every_x, discount_y):
        self.every_x = every_x
        self.discount_y = discount_y

    def apply_discount(self, cart, total):
        total = (total // self.every_x) * self.discount_y
        return total
