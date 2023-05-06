import csv
import tkinter as tk

class Inventory:
    def __init__(self, csv_filename):
        self.items = {}
        with open(csv_filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                item = row['item']
                price = float(row['price'])
                quantity = int(row['quantity'])
                self.items[item] = {'price': price, 'quantity': quantity}

    def check_inventory(self, item):
        return item in self.items and self.items[item]['quantity'] > 0

    def update_inventory(self, item):
        if self.check_inventory(item):
            self.items[item]['quantity'] -= 1

    def get_item_price(self, item):
        if item in self.items:
            return self.items[item]['price']
        else:
            return None

class PaymentManager:
    def __init__(self, cashbox=0, online_account_balance=0):
        self.cashbox = cashbox
        self.online_account_balance = online_account_balance

    def check_cashbox(self):
        return self.cashbox

    def check_online_account_balance(self):
        return self.online_account_balance

    def process_payment(self, payment_method, amount):
        if payment_method == "cash":
            self.cashbox += amount
        elif payment_method == "credit":
            self.online_account_balance += amount

    def return_change(self, change):
        if self.check_cashbox() >= change:
            self.cashbox -= change
            return change
        else:
            return 0

class VendingMachine:
    def __init__(self, inventory, payment_manager):
        self.inventory = inventory
        self.payment_manager = payment_manager

    def show_menu(self):
        print("Welcome to the vending machine!")
        print("Here are the available items and their prices:")
        for item, data in self.inventory.items.items():
            print(f"{item}: ${data['price']:.2f}")

    def get_selection(self):
        while True:
            selection = input("Please enter the name of the item you want: ")
            if self.inventory.check_inventory(selection):
                return selection
            else:
                print("Sorry, that item is not available.")

    def get_payment_method(self):
        while True:
            payment_method = input("Please select a payment method (cash or credit): ").lower()
            if payment_method in ["cash", "credit"]:
                return payment_method
            else:
                print("Invalid payment method. Please try again.")

    def process_payment(self, selection, payment_method):
        price = self.inventory.get_item_price(selection)
        if price is None:
            print("Sorry, the item price is not available.")
            return False

        if payment_method == "cash":
            while True:
                amount = float(input(f"Please insert ${price:.2f}: "))
                if amount >= price:
                    change = amount - price
                    self.payment_manager.process_payment(payment_method, price)
                    print(f"Thank you for your purchase! Here's your {selection}.")
                    if change > 0:
                        change = self.payment_manager.return_change(change)
                        print(f"Don't forget your change: ${change:.2f}")
                    return True
                else:
                    print("Please insert more money.")
        elif payment_method == "credit":
            print(f"Thank you for your purchase! You have been charged ${price:.2f} to your credit card.")
            self.payment_manager.process_payment(payment_method, price)
            print(f"Here's your {selection}.")
            return True
        else:
            print("Sorry,we do not accept that payment method.")
            return False
        
    def dispense_item(self, selection):
        self.inventory.update_inventory(selection)

    def run_vending_machine(self):
        self.show_menu()
        selection = self.get_selection()
        payment_method = self.get_payment_method()
        successful_payment = self.process_payment(selection, payment_method)
        if successful_payment:
            self.dispense_item(selection)


class VendingMachineGUI:
    def __init__(self, vending_machine):
        self.vending_machine = vending_machine
        self.root = tk.Tk()
        self.root.title("Vending Machine")

        self.create_widgets()
        self.root.mainloop()

    def create_widgets(self):
        menu_label = tk.Label(self.root, text="Available items and their prices:")
        menu_label.grid(row=0, column=0, sticky="w", pady=(10, 5))

        item_buttons = {}
        for index, (item, data) in enumerate(self.vending_machine.inventory.items.items(), start=1):
            button_text = f"{item}: ${data['price']:.2f}"
            item_buttons[item] = tk.Button(self.root, text=button_text, command=lambda i=item: self.select_item(i))
            item_buttons[item].grid(row=index, column=0, sticky="w", pady=5)

        self.result_text = tk.StringVar()
        self.result_label = tk.Label(self.root, textvariable=self.result_text, wraplength=300)
        self.result_label.grid(row=1, column=1, rowspan=len(item_buttons), padx=(10, 0), pady=5)

    def select_item(self, item):
        if not self.vending_machine.inventory.check_inventory(item):
            self.result_text.set(f"Sorry, {item} is not available.")
            return

        payment_method = self.vending_machine.get_payment_method()
        successful_payment = self.vending_machine.process_payment(item, payment_method)

        if successful_payment:
            self.vending_machine.dispense_item(item)
            self.result_text.set(f"Thank you for your purchase! Here's your {item}.")
        else:
            self.result_text.set("Payment unsuccessful. Please try again.")

csv_filename = "vending_machine/inventory.csv"
inventory = Inventory(csv_filename)
payment_manager = PaymentManager()
vending_machine = VendingMachine(inventory, payment_manager)
vending_machine_gui = VendingMachineGUI(vending_machine)
