
class OrderService:
    def process_order(self, order, user, discount, is_vip, is_active, payment_method):
        total = 0

        if is_active:
            if user:
                if order:
                    for item in order:
                        if item["quantity"] > 0:
                            if item["price"] > 0:
                                total += item["quantity"] * item["price"]

        if discount:
            if is_vip:
                total -= total * 0.20
            else:
                total -= total * 0.10

        if payment_method == "card":
            if total > 0:
                print("Processing card payment")
            else:
                print("Invalid total")
        elif payment_method == "cash":
            print("Processing cash payment")
        else:
            print("Unsupported payment method")

        return total

    def x(self, a, b, c):
        result = a + b
        return result * c
