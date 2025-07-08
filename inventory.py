from tabulate import tabulate

class Shoe:

    # Constructor method with instance variables 
    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = int(cost)
        self.quantity = int(quantity)

    def get_cost(self):
        """
        Returns the cost of the shoe.
        """
        return self.cost

    def get_quantity(self):
        """
        Returns the quantity of shoes in stock.
        """
        return self.quantity

    def __str__(self):
        """
        Returns a string representation of the shoe.
        """
        return f"{self.country}, {self.code}, {self.product}, " \
               f"{self.cost}, {self.quantity}"


shoe_list = []


def read_shoes_data():
    """
    Loads shoe stock data from a file and populates the shoe_list.
    """
    try:
        # Open the inventory file in read/write mode
        with open(
            "/Users/rolandcrouch/Documents/Hyperion Module 1/"
            "inventory.txt", "r+"
        ) as file:
            next(file)  # Skip the header row

            for line in file:
                # Clean and split each line by commas
                fields = [f.strip() for f in line.strip().split(",")]

                # Validate that each line has exactly 5 fields
                if len(fields) != 5:
                    raise ValueError("Invalid line format")

                # Unpack the cleaned fields into variables
                country, code, product, cost, quantity = fields

                # Create a Shoe object and add it to the list
                shoe_list.append(
                    Shoe(country, code, product, cost, quantity)
                )

    except FileNotFoundError:
        return "\nPlease ensure file is saved correctly"


def write_shoes_data():
    """
    Overwrites the inventory file with current shoe_list data.
    """
    with open(
        "/Users/rolandcrouch/Documents/Hyperion Module 1/"
        "inventory.txt", "w"
    ) as file:
        # Write header line
        file.write("Country,Code,Product,Cost,Quantity\n")

        # Loop through all shoes and write to file
        for shoe in shoe_list:
            file.write(
                f"{shoe.country},{shoe.code},{shoe.product},"
                f"{shoe.cost},{shoe.quantity}\n"
            )


def capture_shoes():
    """
    Captures a new shoe entry from user input and saves to file.
    """
    print("\nPlease enter in your SKU below:\n")

    # Prompt user for input values
    country = input("Which country is this shoe for?\n")
    code = input("Enter a unique product code:\n")

    # Prevent duplication based on code
    if any(shoe.code == code for shoe in shoe_list):
        print("\nThat code already exists. Try a different one.")
        return

    # Get remaining fields from user
    product = input("Enter product name:\n")
    cost = input("Enter total stock value:\n")
    quantity = input("Enter stock quantity:\n")

    # Create and add the new shoe object
    new_shoe = Shoe(country, code, product, cost, quantity)
    shoe_list.append(new_shoe)

    try:
        # Append the new entry to the file
        with open(
            "/Users/rolandcrouch/Documents/Hyperion Module 1/"
            "inventory.txt", "a"
        ) as file:
            file.write(
                f"{new_shoe.country},{new_shoe.code},"
                f"{new_shoe.product},{new_shoe.cost},"
                f"{new_shoe.quantity}\n"
            )
        print("\nNew shoe saved to inventory.")

    except Exception as e:
        print(f"\nError writing to file: {e}")


def view_all():
    """
    Displays all current shoe records in a formatted table.
    """
    if not shoe_list:
        print("\nNo shoes to display.")
        return

    table = []

    # Build rows for tabulation
    for shoe in shoe_list:
        row = [
            shoe.country, shoe.code, shoe.product,
            shoe.cost, shoe.quantity
        ]
        table.append(row)

    headers = ["Country", "Code", "Product", "Cost", "Quantity"]
    print("\n")
    print(tabulate(table, headers, tablefmt="fancy_outline"))


def re_stock():
    """
    Finds and restocks the shoe with the lowest quantity.
    """
    while True:
        # Identify shoe with the smallest quantity
        lowest_stock = min(
            shoe_list, key=lambda shoe: int(shoe.quantity)
        )

        print(f"\nLowest stock:\n\n{lowest_stock}")
        u_input = input(
            "\nType 'y' to restock or anything else to cancel: "
        )

        if u_input.lower() == "y":
            try:
                # Ask how many items to add
                stock_to_add = int(input("\nHow many to add?: "))

                # Add the new stock to the quantity
                lowest_stock.quantity += stock_to_add

                print(
                    f"\nStock updated: {lowest_stock.code} now has "
                    f"{lowest_stock.quantity} items."
                )

                # Save the update to the file
                write_shoes_data()

            except ValueError:
                print("\nPlease enter a valid number.")
        else:
            break


def search_shoe():
    """
    Allows user to look up a shoe using its product code.
    """
    while True:
        target = input(
            "\nEnter product code or 'R' to return to menu:\n"
        )

        if target.lower() == 'r':
            break

        # Loop through shoes to find a match
        for shoe in shoe_list:
            if shoe.code == target:
                headers = ["Country", "Code", "Product",
                           "Cost", "Quantity"]
                row = [[
                    shoe.country, shoe.code, shoe.product,
                    shoe.cost, shoe.quantity
                ]]
                print(tabulate(row, headers, tablefmt="fancy_outline"))


def value_per_item():
    """
    Calculates and displays value of each shoe item.
    """
    table = []

    for shoe in shoe_list:
        # Compute total value = cost * quantity
        value = shoe.cost * shoe.quantity

        row = [
            shoe.country, shoe.code, shoe.product,
            shoe.cost, shoe.quantity, "{:,}".format(value)
        ]
        table.append(row)

    headers = [
        "Country", "Code", "Product", "Cost", "Quantity", "Value"
    ]
    print("\n")
    print(tabulate(table, headers, tablefmt="fancy_outline"))


def highest_qty():
    """
    Displays the product with the highest stock level.
    """
    highest = max(shoe_list, key=lambda shoe: shoe.quantity)
    print(f"\nThe {highest.product} in {highest.country} "
          f"are on sale with a quantity of {highest.quantity}.")
    
def print_main_menu():
    """
    Displays the main menu with ANSI colors and structure.
    """
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

    print(f"\n{BOLD}{CYAN}╔════════════════════════════════════════════"
          f"══╗{RESET}")
    print(f"{BOLD}{CYAN}║{RESET}          {BOLD}{BLUE}NIKE STOCK MANAGE"
          f"MENT MENU{RESET}          {CYAN}║{RESET}")
    print(f"{BOLD}{CYAN}╠══════════════════════════════════════════════"
          f"╣{RESET}")
    print(f"{BOLD}{CYAN}║{RESET}  {GREEN}1.{RESET} Add a new shoe to st"
          f"ock records          {CYAN}║{RESET}")
    print(f"{BOLD}{CYAN}║{RESET}  {GREEN}2.{RESET} View all shoes in st"
          f"ock                  {CYAN}║{RESET}")
    print(f"{BOLD}{CYAN}║{RESET}  {GREEN}3.{RESET} Restock the lowest-s"
          f"tock shoe            {CYAN}║{RESET}")
    print(f"{BOLD}{CYAN}║{RESET}  {GREEN}4.{RESET} Search for a shoe by"
           f" product code        {CYAN}║{RESET}")
    print(f"{BOLD}{CYAN}║{RESET}  {GREEN}5.{RESET} View total stock val"
          f"ue of each shoe      {CYAN}║{RESET}")
    print(f"{BOLD}{CYAN}║{RESET}  {GREEN}6.{RESET} Display shoe with hi"
          f"ghest stock          {CYAN}║{RESET}")
    print(f"{BOLD}{CYAN}║{RESET}  {GREEN}7.{RESET} Exit the Stock App"
           f"                       {CYAN}║{RESET}")
    print(f"{BOLD}{CYAN}╚══════════════════════════════════════════════"
          f"╝{RESET}")

def stock_app():
    """
    Launches the Nike stock management system and handles
    user input to perform stock operations.
    """
    print("\nWelcome to the Nike Stock App!")
    print("\nWe will now upload your stock records.")
    choice = input("\nType Y to proceed: ")

    if choice.lower() != 'y':
        print("\nGoodbye! Stock App closed.")
        return

    # Load shoe data from file
    read_shoes_data()
    print("\nStock records uploaded successfully!")

    while True:
        # Display menu and get user input
        print_main_menu()
        choice = input("\nEnter a number (1–7): ")

        # Call function based on user input
        if choice == '1':
            capture_shoes()
        elif choice == '2':
            view_all()
        elif choice == '3':
            re_stock()
        elif choice == '4':
            search_shoe()
        elif choice == '5':
            value_per_item()
        elif choice == '6':
            highest_qty()
        elif choice == '7':
            print("\nYou have exited the Stock App. Goodbye!\n")
            break
        else:
            print("\nInvalid input. Please enter a number from 1 to 7.")


# Start the stock application
stock_app()




