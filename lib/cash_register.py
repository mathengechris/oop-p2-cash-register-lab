class CashRegister:
    def __init__(self, discount=0):
        self._discount = 0
        self.discount = discount
        
        self.total = 0.0
        self.items = []
        self.previous_transactions = []

    # --- Properties for Validation ---
    @property
    def discount(self):
        return self._discount

    @discount.setter
    def discount(self, value):
        if not isinstance(value, int):
            print("Not valid discount")
            return
        
        if 0 <= value <= 100:
            self._discount = value
        else:
            print("Not valid discount")

    # --- Methods ---
    def add_item(self, item, price, quantity=1):
        """Adds price * quantity to total, appends item name multiple times, logs to history."""
        item_cost = price * quantity
        self.total += item_cost
        
        # If quantity is multiple, add the item string multiple times to the list
        for _ in range(quantity):
            self.items.append(item)
        
        # Save transaction data for a precise void rollback later
        transaction_record = {
            "item": item,
            "price": price,
            "quantity": quantity
        }
        self.previous_transactions.append(transaction_record)

    def apply_discount(self):
        """Applies percentage reduction and prints the exact expected success string."""
        if self.discount == 0:
            print("There is no discount to apply.")
            return

        discount_amount = self.total * (self.discount / 100)
        self.total -= discount_amount
        
        # Format matching the assertion: "After the discount, the total comes to $X."
        # Using :.2f ensures trailing decimals map nicely if required, or fallback to integer formatting if it strictly expects integers like $800.
        # Let's use clean matching formatting based on the test case:
        formatted_total = int(self.total) if self.total.is_integer() else round(self.total, 2)
        print(f"After the discount, the total comes to ${formatted_total}.")

    def void_last_transaction(self):
        """Removes the last transaction record entirely and reverts total and items arrays."""
        if not self.previous_transactions:
            return

        # Pop the last transaction record
        last_tx = self.previous_transactions.pop()
        
        # Deduct its full cost from total
        self.total -= (last_tx["price"] * last_tx["quantity"])
        
        # Remove the item name from the items list exactly as many times as its quantity
        for _ in range(last_tx["quantity"]):
            if last_tx["item"] in self.items:
                self.items.remove(last_tx["item"])