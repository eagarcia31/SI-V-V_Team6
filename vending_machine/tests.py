import csv
import unittest
from vending_machine import Inventory, PaymentManager, VendingMachine

class Tests(unittest.TestCase):

    def test_check_inventory_black_box(self):
        inventory = Inventory("vending_machine/inventory.csv")

        # TC1 - check if item has available inventory
        item_available = "Coke"
        self.assertTrue(inventory.check_inventory(item_available), f"Test case 1 - Check Inventory (Black Box): Item '{item_available}' is not available")
        print(f"Test case 1 - Check Inventory (Black Box): Item '{item_available}' is available")

        # TC2 - check if item has no available inventory
        item_not_available = "Water"
        self.assertFalse(inventory.check_inventory(item_not_available), f"Test case 2 - Check Inventory (Black Box): Item '{item_not_available}' is available")
        print(f"Test case 2 - Check Inventory (Black Box): Item '{item_not_available}' is not available")

        # TC3 - check item with quantity 0
        item_quantity_zero = "Snacks"
        self.assertFalse(inventory.check_inventory(item_quantity_zero), f"Test case 3 - Check Inventory (Black Box): Item '{item_quantity_zero}' has available inventory")
        print(f"Test case 3 - Check Inventory (Black Box): Item '{item_quantity_zero}' has a quantity of 0")

    def test_update_inventory_white_box(self):
        inventory = Inventory("vending_machine/inventory.csv")

        # TC4 - update inventory for item
        item_available = "Coke"
        initial_quantity = inventory.items[item_available]['quantity']
        inventory.update_inventory(item_available)
        updated_quantity = inventory.items[item_available]['quantity']
        self.assertEqual(updated_quantity, initial_quantity - 1, f"Test case 4 - Update Inventory (White Box): Item '{item_available}' inventory not updated")
        print(f"Test case 4 - Update Inventory (White Box): Item '{item_available}' inventory updated")

        # TC5 - update inventory for an unavailable item
        item_unavailable = "Water"
        initial_quantity = inventory.items[item_unavailable]['quantity']
        inventory.update_inventory(item_unavailable)
        updated_quantity = inventory.items[item_unavailable]['quantity']
        self.assertEqual(updated_quantity, initial_quantity, f"Test case 5 - Update Inventory (White Box): Item '{item_unavailable}' inventory updated")
        print(f"Test case 5 - Update Inventory (White Box): Item '{item_unavailable}' inventory not updated")

    def test_get_item_price_white_box(self):
        inventory = Inventory("vending_machine/inventory.csv")

        # TC6 - get price for an available item
        item_available = "Coke"
        item_price = inventory.get_item_price(item_available)
        self.assertIsNotNone(item_price, f"Test case 6 - Get Item Price (White Box): Item '{item_available}' price is None")
        print(f"Test case 6 - Get Item Price (White Box): Item '{item_available}' price: {item_price}")

        # TC7 - get price for an unavailable item
        item_unavailable = "Water"
        item_price = inventory.get_item_price(item_unavailable)
        self.assertIsNone(item_price, f"Test case 7 - Get Item Price (White Box): Item '{item_unavailable}' price is not None")
        print(f"Test case 7 - Get Item Price (White Box): Item '{item_unavailable}' price is None")

    def test_return_change_black_box(self):
        payment_manager = PaymentManager(cashbox=30.0)

        # TC8 - sufficient cash in cashbox
        change = 10.0
        returned_change = payment_manager.return_change(change)
        self.assertEqual(returned_change, change, f"Test case 8 - Return Change (Black Box): Incorrect returned change. Expected: {change}, Actual: {returned_change}")
        self.assertEqual(payment_manager.check_cashbox(), 20.0, f"Test case 8 - Return Change (Black Box): Cashbox not updated correctly. Expected: 20.0, Actual: {payment_manager.check_cashbox()}")
        print(f"Test case 8 - Return Change (Black Box): Returned change: {returned_change}")

        # TC9 - insufficient cash in cashbox
        change = 40.0
        returned_change = payment_manager.return_change(change)
        self.assertEqual(returned_change, 0, f"Test case 9 - Return Change (Black Box): Incorrect returned change. Expected: 0, Actual: {returned_change}")
        self.assertEqual(payment_manager.check_cashbox(), 20.0, f"Test case 9 - Return Change (Black Box): Cashbox not updated correctly. Expected: 20.0, Actual: {payment_manager.check_cashbox()}")
        print(f"Test case 9 - Return Change (Black Box): Returned change: {returned_change}")

    def test_vending_machine_black_box(self):
        vm = VendingMachine("vending_machine/inventory.csv", 50.0)

        # TC10 - successful transaction
        item_to_purchase = "Coke"
        payment = 5.0
        expected_change = payment - vm.inventory.get_item_price(item_to_purchase)
        purchased, change = vm.purchase_item(item_to_purchase, payment)
        self.assertTrue(purchased, f"Test case 10 - Vending Machine (Black Box): Item '{item_to_purchase}' not purchased")
        self.assertEqual(change, expected_change, f"Test case 10 - Vending Machine (Black Box): Incorrect change. Expected: {expected_change}, Actual: {change}")
        print(f"Test case 10 - Vending Machine (Black Box): Item '{item_to_purchase}' purchased, change: {change}")

        # TC11 - insufficient payment
        item_to_purchase = "Coke"
        payment = 1.0
        purchased, change = vm.purchase_item(item_to_purchase, payment)
        self.assertFalse(purchased, f"Test case 11 - Vending Machine (Black Box): Item '{item_to_purchase}' purchased with insufficient payment")
        self.assertEqual(change, payment, f"Test case 11 - Vending Machine (Black Box): Incorrect change. Expected: {payment}, Actual: {change}")
        print(f"Test case 11 - Vending Machine (Black Box): Item '{item_to_purchase}' not purchased, change: {change}")

if __name__ == '__main__':
    unittest.main()

