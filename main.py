import json

from Discount import Coupon, OnTop, Seasonal


def print_receipt(cart, campaigns):
    # Display cart items
    total = 0
    print("Items in cart:")
    for item in cart:
        print(f"{item['quantity']} {item['item']}: {item['quantity'] * item['price']} THB")
        total += item['quantity'] * item['price']

    # Apply discount and display
    print()
    for discount in campaigns:
        discount_value = discount.apply_discount(cart, total)
        if isinstance(discount, Coupon):
            if discount.discount_type == "Fixed":
                print(f"Discount: {discount_value} THB")
            else:
                print(f"Discount: {discount_value}%")
        elif isinstance(discount, OnTop):
            if discount.discount_type == "PercentageByItemCategory":
                print(f"Discount: {discount.value}% Off on {discount.category}")
            elif discount.discount_type == "DiscountByPoints":
                print(f"Points: {discount.value} Points")
        elif isinstance(discount, Seasonal):
            print(f"Discount: {discount.discount_y} THB at every {discount.every_x} THB")
        total -= discount_value

    print(f"\nTotal Price: {total} THB")


def process_discounts():
    with open('shopping_cart.json', 'r') as f:
        cart = json.load(f)

    with open('discount_campaigns.json', 'r') as f:
        campaign_data = json.load(f)

    campaigns = [None] * 3
    for data in campaign_data:
        if data['type'] == 'Coupon':
            campaigns[0] = (Coupon(data['discount_type'], data['value']))
        elif data['type'] == 'OnTop':
            if data.get('discount_type') == "DiscountByPoints":
                campaigns[1] = (OnTop(data['discount_type'], None, data['value']))
            else:
                campaigns[1] = (OnTop(data['discount_type'], data['category'], data['value']))
        elif data['type'] == 'Seasonal':
            campaigns[2] = (Seasonal(data['every_x'], data['discount_y']))

    print_receipt(cart, campaigns)


if __name__ == "__main__":
    process_discounts()
