from inventory import Inventory
from supplier import Supplier
from DiscountStrategy import NoDiscount, PercentageDiscount, BulkDiscount, StudentDiscount
from productfactory import ProductFactory
from order import Order
from orderline import OrderLine
import csv


# ============================================================
# 1. LOAD PRODUCTS FROM CSV
# ============================================================

def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    loaded = 0
    try:
        file = open(path, newline="")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        with file:
            reader = csv.reader(file)
            next(reader, None)  # Skip header row
            for row in reader:
                try:
                    product_type = row[0]
                    product_id = row[1]
                    name = row[2]
                    price = float(row[3])
                    stock = int(row[4])
                    if product_type.lower() == "physical":
                        extra_attribute = 1.5
                    elif product_type.lower() == "digital":
                        extra_attribute = 5000
                    else:
                        extra_attribute = 0
                    product = ProductFactory.create(
                        product_type,
                        product_id,
                        product_type,
                        name,
                        price,
                        stock,
                        extra_attribute,
                        supplier=supplier
                    )
                    inventory.add_product(product)
                    loaded += 1
                except ValueError as error:
                    print(f"Skipping row {row}: {error}")
        print("products loaded.")
    finally:
        print("Load attempt finished.")

def get_positive_float(prompt: str) -> float:

    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")

Supplier1 = Supplier(
    "S001",
    "Supplier 1",
    "Supplier1@supplier1.com"
)

Supplier2 = Supplier(
    "S002",
    "Supplier 2",
    "Supplier2@supplier2.com"
)

Supplier3 = Supplier(
    "S003",
    "Supplier 3",
    "Supplier3@supplier3.com"
)

print("\n========== PRODUCT FACTORY ==========")
physicalProduct1 = ProductFactory.create(
    "physical",
    "P001", "physical", "Phone", 1000, 10, 1.5,
    supplier=Supplier1
)
digitalProduct1 = ProductFactory.create(
    "digital",
    "P002", "digital", "Software", 1000, 10, 5000,
    supplier=Supplier2
)

print("Physical and digital products created successfully.")

inventory1 = Inventory()
inventory1.add_product(physicalProduct1)
inventory1.add_product(digitalProduct1)

print("\n========== INVENTORY INFORMATION ==========")

for product in inventory1.products:
    product.display_information()
    print(product.get_fulfilment_info())
    print("=========================================")


print("\n============= PRINT PRODUCTS IN INVENTORY ==============")

inventory1.display_all_products()

print("========================================================")


# ============================================================
# 6. TEST STRATEGY PATTERN
# ============================================================

print("\n========== STRATEGY PATTERN ==========")
strategyProduct1 = ProductFactory.create(
    "physical",
    "P100", "physical", "Keyboard", 100, 10, 1.5,
    supplier=Supplier1
)
strategyProduct2 = ProductFactory.create(
    "digital",
    "P101", "digital", "Software", 50, 10, 5000,
    supplier=Supplier2
)

order = Order(
    "Order_001",
    BulkDiscount(200, 20)
)
order.add_order_line(strategyProduct1, 2)
order.add_order_line(strategyProduct2, 1)

print("\nOriginal total: 250")
print("BulkDiscount(200, 20):")
print(order.calculate_total())
print("\n========== CHANGE DISCOUNT STRATEGY ==========")

order.set_discount(PercentageDiscount(10))

print("PercentageDiscount(10):")
print(order.calculate_total())


# ============================================================
# 8. TEST NEW DISCOUNT STRATEGY
# ============================================================

print("\n========== STUDENT DISCOUNT ==========")
order.set_discount(StudentDiscount())
print("StudentDiscount(15%):")
print(order.calculate_total())

print("\n========== NO DISCOUNT ==========")
order.set_discount(NoDiscount())
print("NoDiscount: ", order.calculate_total())


print("\n========== DEFAULT DISCOUNT ==========")
defaultOrder = Order("Order_002")
defaultOrder.add_order_line(strategyProduct1, 2)
defaultOrder.add_order_line(strategyProduct2, 1)

print("DefaultDiscount: ", defaultOrder.calculate_total())

print("\n========== UNKNOWN PRODUCT TYPE ==========")
try:
    invalidProduct = ProductFactory.create(
        "service",
        "P200", "service", "Installation", 30, 5, 0,
        supplier=Supplier3
    )
except ValueError as error:
    print(error)

print("\n========== INVALID PRODUCT PRICE ==========")
try:
    invalidPriceProduct = ProductFactory.create(
        "physical",
        "P201", "physical", "Phone", 0, 10, 1.5,
        supplier=Supplier1
    )
except ValueError as error:
    print(error)

print("\n========== INVALID PRODUCT STOCK ==========")
try:
    invalidStockProduct = ProductFactory.create(
        "physical",
        "P202", "physical", "Laptop", 1000, -5, 1.5,
        supplier=Supplier1
    )
except ValueError as error:
    print(error)

print("\n========== INVALID ORDERLINE QUANTITY ==========")
try:
    invalidOrderLine = OrderLine(physicalProduct1, 0)
except ValueError as error:
    print(error)

print("\n========== USER INPUT VALIDATION ==========")

print("\n========== LOAD PRODUCTS FROM CSV ==========")

csvInventory = Inventory()
load_products(
    "products.csv",
    csvInventory,
    Supplier1
)
csvInventory.display_all_products()

print("\n========== MISSING FILE TEST ==========")
load_products(
    "missing.csv",
    csvInventory,
    Supplier1
)

