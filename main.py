import itertools
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import unittest


class Car:
    _ids = itertools.count(1)

    def __init__(self, make, model, price):
        self.id = next(self._ids)
        self.make = make
        self.model = model
        self.price = price

    def __str__(self):
        return f'Car {self.id}: {self.make} {self.model}, ${self.price}'

    @property
    def make(self):
        return self._make

    @make.setter
    def make(self, value):
        if not isinstance(value, str):
            raise ValueError("Make must be a string")
        if not value:
            raise ValueError("Make cannot be empty")
        self._make = value

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        if not isinstance(value, str):
            raise ValueError("Model must be a string")
        if not value:
            raise ValueError("Model cannot be empty")
        self._model = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Price must be a number")
        if value < 0:
            raise ValueError("Price cannot be negative")
        self._price = value


class CarDealership:

    def __init__(self):
        self.cars = []

    def add_car(self, car):
        self.cars.append(car)

    def __str__(self):
        return f'CarDealership with cars: {[str(car) for car in self.cars]}'

    def sell_car(self, customer, car_id):
        car = next((car for car in self.cars if car.id == car_id), None)
        if car and customer.buy_car(car):
            self.cars.remove(car)
            contract = SalesContract(customer, car)
            return contract
        return None


class Customer:
    _ids = itertools.count(1)

    def __init__(self, name, balance):
        self.id = next(self._ids)
        self.name = name
        self.balance = balance

    def __str__(self):
        return f'Customer {self.id}: {self.name}, Balance: ${self.balance}'

    def buy_car(self, car):
        if self.balance >= car.price:
            self.balance -= car.price
            return True
        return False

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ValueError("Name must be a string")
        if not value:
            raise ValueError("Name cannot be empty")
        self._name = value

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Balance must be a number")
        if value < 0:
            raise ValueError("Balance cannot be negative")
        self._balance = value


class SalesContract:
    _ids = itertools.count(1)

    def __init__(self, customer, car):
        self.id = next(self._ids)
        self.customer = customer
        self.car = car
        self.date = datetime.now()

    def __str__(self):
        return f'SalesContract {self.id}: {self.customer.name} buys {self.car.make} {self.car.model} on {self.date}'


class TestCar(unittest.TestCase):

    def test_car_creation(self):
        car = Car("Toyota", "Corolla", 20000)
        self.assertEqual(car.make, "Toyota")
        self.assertEqual(car.model, "Corolla")
        self.assertEqual(car.price, 20000)

    def test_car_make_validation(self):
        with self.assertRaises(ValueError):
            Car("", "Corolla", 20000)

    def test_car_price_validation(self):
        with self.assertRaises(ValueError):
            Car("Toyota", "Corolla", -10000)


class TestCarDealership(unittest.TestCase):

    def setUp(self):
        self.dealership = CarDealership()
        self.car1 = Car("Toyota", "Corolla", 20000)
        self.car2 = Car("Honda", "Civic", 18000)
        self.dealership.add_car(self.car1)
        self.dealership.add_car(self.car2)
        self.customer = Customer("John Doe", 25000)

    def test_add_car(self):
        self.assertEqual(len(self.dealership.cars), 2)

    def test_sell_car(self):
        contract = self.dealership.sell_car(self.customer, self.car1.id)
        self.assertIsNotNone(contract)
        self.assertEqual(len(self.dealership.cars), 1)
        self.assertEqual(self.customer.balance, 5000)

    def test_sell_car_insufficient_funds(self):
        self.customer.balance = 10000
        contract = self.dealership.sell_car(self.customer, self.car1.id)
        self.assertIsNone(contract)
        self.assertEqual(len(self.dealership.cars), 2)
        self.assertEqual(self.customer.balance, 10000)


class TestCustomer(unittest.TestCase):

    def test_customer_creation(self):
        customer = Customer("John Doe", 25000)
        self.assertEqual(customer.name, "John Doe")
        self.assertEqual(customer.balance, 25000)

    def test_buy_car(self):
        customer = Customer("John Doe", 25000)
        car = Car("Toyota", "Corolla", 20000)
        self.assertTrue(customer.buy_car(car))
        self.assertEqual(customer.balance, 5000)

    def test_buy_car_insufficient_funds(self):
        customer = Customer("John Doe", 10000)
        car = Car("Toyota", "Corolla", 20000)
        self.assertFalse(customer.buy_car(car))
        self.assertEqual(customer.balance, 10000)


class TestSalesContract(unittest.TestCase):

    def test_contract_creation(self):
        customer = Customer("John Doe", 25000)
        car = Car("Toyota", "Corolla", 20000)
        contract = SalesContract(customer, car)
        self.assertEqual(contract.customer, customer)
        self.assertEqual(contract.car, car)
        self.assertTrue(isinstance(contract.date, datetime))


if __name__ == "__main__":

    unittest.main(exit=False)

    dealership = CarDealership()

    while True:
        print("\n--- Car Dealership Menu ---")
        print("1. Add a Car")
        print("2. List All Cars")
        print("3. Add a Customer")
        print("4. List All Customers")
        print("5. Sell a Car")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            make = input("Enter car make: ")
            model = input("Enter car model: ")
            price = float(input("Enter car price: "))
            car = Car(make, model, price)
            dealership.add_car(car)
            print(f"Car {car} added to the dealership.")

        elif choice == "2":
            print("\nCars in dealership:")
            for car in dealership.cars:
                print(car)

        elif choice == "3":
            name = input("Enter customer name: ")
            balance = float(input("Enter customer balance: "))
            customer = Customer(name, balance)
            print(f"Customer {customer} added.")

        elif choice == "4":
            print("\nCustomers:")

            if 'customers' not in globals():
                customers = []
            for cust in customers:
                print(cust)

        elif choice == "5":
            if 'customers' not in globals():
                print("No customers available. Please add a customer first.")
                continue
            cust_name = input("Enter customer name: ")
            customer = next(
                (cust for cust in customers if cust.name == cust_name), None)
            if not customer:
                print(f"No customer found with name {cust_name}")
                continue
            car_id = int(input("Enter car ID to sell: "))
            contract = dealership.sell_car(customer, car_id)
            if contract:
                print(f"Car sold successfully! Contract: {contract}")
            else:
                print(
                    "Transaction failed. Either car not found or insufficient funds."
                )

        elif choice == "6":
            print("Exiting...")
            break

        else:
            print("Invalid choice, please try again.")
