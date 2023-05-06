import csv
import tkinter as tk
from tkinter import messagebox

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
        self.payment_input = ""

    def show_menu(self):
        print("Welcome to the vending machine!")
        print("Here are the available items and their prices:")
        for item, data in self.inventory.items.items():
            print(f"{item}: ${data['price']:.2f}")

    def get_selection(self):
        while True:
            selection = input("Please enter the name of the item you want: ")
            if self.inventory.check_inventory(selection):
                self.item_selected = selection
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
            return None  # Return None if payment method is invalid


    def process_payment(self, selection, payment_method, amount):
        price = self.inventory.get_item_price(selection)
        if price is None:
            print("Sorry, the item price is not available.")
            return False

        if payment_method == "cash":
            while True:
                if amount >= price:
                    change = amount - price
                    self.payment_manager.process_payment(payment_method, price)
                    # print(f"Thank you for your purchase! Here's your {selection}.")
                    if change > 0:
                        change = self.payment_manager.return_change(change)
                        # print(f"Don't forget your change: ${change:.2f}")
                    return True
                else:
                    print("Please insert more money.")
                    break
        elif payment_method == "credit":
            print(f"Thank you for your purchase! You have been charged ${price:.2f} to your credit card.")
            self.payment_manager.process_payment(payment_method, price)
            print(f"Here's your {selection}.")
            return True
        else:
            print("Sorry, we do not accept that payment method.")
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
    def __init__(self, inventory, vending_machine,):
        self.vending_machine = vending_machine
        self.root = tk.Tk()
        self.root.title("Vending Machine")
        self.item_selected = "" 
        self.payment_method_selected = False 
        self.inventory = inventory

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
        self.result_label.grid(row=7, column=1, rowspan=len(item_buttons), padx=(10, 0), pady=5)

    def create_payment_widgets(self):
        self.payment_text = ""
        payment_label = tk.Label(self.root, text="Payment Method:")
        payment_label.grid(row=0, column=1, sticky="w", pady=(10, 5))

        cash_button = tk.Button(self.root, text="Cash", command=self.select_cash_payment)
        cash_button.grid(row=1, column=1, sticky="w", pady=5)

        credit_button = tk.Button(self.root, text="Credit", command=self.select_credit_payment)
        credit_button.grid(row=2, column=1, sticky="w", pady=5)

    def create_cash_widgets(self):
        price = self.inventory.get_item_price(self.item_selected)
        # self.payment_text = ""
        self.payment_label = tk.Label(self.root, textvariable=self.payment_text)
        self.payment_label.grid(row=3, column=1, sticky="w", pady=5)

        self.amount_label = tk.Label(self.root, text="Enter ${:.2f}:".format(price))
        self.amount_label.grid(row=4, column=1, sticky="w", pady=5)

        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.grid(row=5, column=1, sticky="w", pady=5)

        self.pay_button = tk.Button(self.root, text="Pay", command=self.process_payment)
        self.pay_button.grid(row=6, column=1, sticky="w", pady=5)

    def hide_cash_widgets(self):
        self.payment_label.grid_forget()
        self.amount_label.grid_forget()
        self.amount_entry.grid_forget()
        self.pay_button.grid_forget()

    def select_item(self, item):
        if not self.vending_machine.inventory.check_inventory(item):
            self.result_text.set(f"Sorry, {item} is not available.\n\nPlease select another item!")
            return
        else:
            self.result_text.set(f"You've selected {item}.\nPlease select a payment method above.")
            self.item_selected = item  # Update the item_selected attribute
            self.create_payment_widgets()  # Display payment method buttons

    def select_cash_payment(self):
        self.payment_text = "cash"
        self.create_cash_widgets()  # Display cash input field

    def select_credit_payment(self):
        self.payment_text = "credit"
        self.create_cash_widgets()  # Display cash input field
        self.hide_cash_widgets()  # Hide cash input field

        self.pay_button = tk.Button(self.root, text="Pay", command=self.process_payment)
        self.pay_button.grid(row=6, column=1, sticky="w", pady=5)

    def hide_credit_widgets(self):
        # Add code to hide credit input widgets
        pass


    def process_payment(self):
        print("inside")
        selection = self.item_selected
        payment_method = self.payment_text
        print(payment_method)

        if payment_method == "cash":
            amount = float(self.amount_entry.get())

            successful_payment = self.vending_machine.process_payment(selection, payment_method, amount)

            if successful_payment:
                self.vending_machine.dispense_item(selection)
                self.hide_cash_widgets()
                self.result_text.set(f"Thank you for your purchase!\nHere's your {selection}.\n\nSelect a new item if you'd like!")
            else:
                self.result_text.set("Payment unsuccessful. Please try again.")
                print("NAR")

        elif payment_method == "credit":
            successful_payment = self.vending_machine.process_payment(selection, payment_method, 0)
            price = self.inventory.get_item_price(self.item_selected)

            if successful_payment:
                self.vending_machine.dispense_item(selection)
                self.hide_cash_widgets()
                # self.result_text.set(f"Thank you for your purchase!\nHere's your {selection}.\n\nSelect a new item if you'd like!")
                self.result_text.set(f"Thank you for your purchase!\nYou have been charged ${price:.2f} to your credit card.\nHere's your {selection}.\n\nSelect a new item if you'd like!" )
            else:
                self.result_text.set("Payment unsuccessful. Please try again.")


csv_filename = "vending_machine/inventory.csv"
inventory = Inventory(csv_filename)
payment_manager = PaymentManager()
vending_machine = VendingMachine(inventory, payment_manager)
vending_machine_gui = VendingMachineGUI(inventory, vending_machine)
