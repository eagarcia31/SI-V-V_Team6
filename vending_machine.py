# Define a dictionary of available items and their prices
ITEM_PRICES = {'Coke': 1.50, 'Pepsi': 1.25, 'Water': 1.00}

# Display the available items and their prices
def show_menu():
    """Display the available items and their prices to the user."""
    print("Welcome to the vending machine!")
    print("Here are the available items and their prices:")
    for item, price in ITEM_PRICES.items():
        print(f"{item}: ${price:.2f}")

# Get the user's selection and validate it
def get_selection():
    """Prompt the user to select an item and validate their input."""
    while True:
        selection = input("Please enter the name of the item you want: ")
        if selection in ITEM_PRICES:
            return selection
        else:
            print("Sorry, that item is not available.")

# Process the user's payment and dispense the selected item
def process_payment(selection, payment_method):
    """Process the user's payment and dispense the selected item."""
    price = ITEM_PRICES[selection]
    if payment_method == "cash":
        while True:
            amount = float(input(f"Please insert ${price:.2f}: "))
            if amount >= price:
                change = amount - price
                print(f"Thank you for your purchase! Here's your {selection}.")
                if change > 0:
                    print(f"Don't forget your change: ${change:.2f}")
                break
            else:
                print("Please insert more money.")
    elif payment_method == "credit":
        print(f"Thank you for your purchase! You have been charged ${price:.2f} to your credit card.")
        print(f"Here's your {selection}.")
    else:
        print("Sorry, we do not accept that payment method.")

# Main function to run the simulation
def run_vending_machine():
    """Run the vending machine simulation."""
    show_menu()
    selection = get_selection()
    payment_method = input("Please select a payment method (cash or credit): ")
    process_payment(selection, payment_method)

# Run the simulation
run_vending_machine()
