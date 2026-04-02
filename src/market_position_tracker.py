import json
from pathlib import Path

# Path to the portfolio data file
DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "portfolio.json"


def load_portfolio():
    """
    Load portfolio data from the JSON file.
    If the file does not exist, create a default one.
    """
    if not DATA_FILE.exists():
        default_data = {
            "starting_balance": 20.0,
            "current_balance": 20.0,
            "open_positions": [],
            "trade_history": []
        }
        save_portfolio(default_data)
        return default_data
    
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)
    

def save_portfolio(data):
    """
    Save portfolio data to the JSON file.
    """
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def show_menu():
    """
    Display the main CLI menu.
    """
    print("\n=== Market Position Tracker ===")
    print("1. View balnce and performance")
    print("2. Log a buy")
    print("3. Log a sell")
    print("4. View open positions")
    print("5. Check current value of a position")
    print("6. view trade history")
    print("7. Reset account")
    print("0. Exit")


def view_balance(data):
    """
    Show the current account overview.
    """
    print("\n--- Balance Overview ---")
    print(f"Starting Balance: ${data['starting_balance']:.2f}")
    print(f"Current Balance:  ${data['current_balance']:.2f}")
    print(f"Open Positions:   {len(data['open_positions'])}")
    print(f"Closed Trades:    {len(data['trade_history'])}")



def log_buy(data):
    """
    Log a new buy position and update the portfolio.
    """
    print("\n--- Log a Buy ---")

    market_name = input("Enter market name: ").strip()
    side = input("Enter side (YES/NO): ").strip().upper()

    if side not in ["YES", "NO"]:
        print("\nInvaild side. Please enter YES or NO.")
        return
    
    try:
        entry_price = float(input("Enter entry price (example: 0.45): ").strip())
        amount_spent = float(input("Enter amount to spend: ").strip())
    except ValueError:
        print("\nInvaild number entered. Please try again.")
        return
    
    if entry_price <= 0 or entry_price >= 1:
        print("\nEntry price must be greater than 0 and less than 1.")
        return
    
    if amount_spent <= 0:
        print("\nAmount spent must be greater than 0.")
        return
    
    if amount_spent > data["current_balance"]:
        print("\nNot enough balance for this trade.")
        return
    
    contracts = amount_spent / entry_price

    position = {
        "market_name": market_name,
        "side": side,
        "entry_price": entry_price,
        "amount_spent": amount_spent,
        "contracts": contracts,
        "status": "OPEN"
    }

    data["open_positions"].append(position)
    data["current_balance"] -= amount_spent
    save_portfolio(data)

    print("\nBuy logged successfully.")
    print(f"Market:         {market_name}")
    print(f"Side:           {side}")
    print(f"Entry Price:    ${entry_price:.2f}")
    print(f"Amount Spent:   ${amount_spent:.2f}")
    print(f"Contracts:      {contracts:.4f}")
    print(f"New Balance:    ${data['current_balance']:.2f}")



def view_open_positions(data):
    """
    Display all currently open positions.
    """
    print("\n--- Open Positions ---")

    open_positions = data["open_positions"]

    if not open_positions:
        print("No open positions found.")
        return
    
    for index, position in enumerate(open_positions, start=1):
        print(f"\nPosition #{index}")
        print(f"Market:         {position['market_name']}")
        print(f"Side:           {position['side']}")
        print(f"Entry Price:    ${position['entry_price']:.2f}")
        print(f"Amount Spent:   ${position['amount_spent']:.2f}")
        print(f"Contracts:      {position['contracts']:.4f}")
        print(f"Status:         {position['status']}")


def check_position_value(data):
    """
    Check current value of an open position without selling it.
    """
    print("\n--- Check Position Value ---")

    open_positions = data["open_positions"]

    if not open_positions:
        print("No open positions available.")
        return
    
    for index, position in enumerate(open_positions, start=1):
        print(f"{index}. {position['market_name']} ({position['side']})")

    try:
        selection = int(input("\nSelect a position number: ").strip())
    except ValueError:
        print("\nInvaild selection. Please enter a number.")
        return
    
    if selection < 1 or selection > len(open_positions):
        print("\nSelected position does not exist.")
        return
    
    position = open_positions[selection - 1]

    try:
        current_price = float(input("Enter current price: ").strip())
    except ValueError:
        print("\nInvaild price entered.")
        return
    
    if current_price <= 0 or current_price >= 1:
        print("\nCurrent price must be greater than 0 and less than 1.")
        return
    
    current_value = position["contracts"] * current_price
    profit_loss = current_value - position["amount_spent"]
    return_percent = (profit_loss / position["amount_spent"]) * 100

    print("\n--- Position Value ---")
    print(f"Market:             {position['market_name']}")
    print(f"Side:               {position['side']}")
    print(f"Entry Price:        ${position['entry_price']:.2f}")
    print(f"Current Price:      ${current_price:2f}")
    print(f"Amount Spent:       ${position['amount_spent']:.2f}")
    print(f"Contracts:          {position['contracts']:.4f}")
    print(f"Current Value:      ${current_value:.2f}")
    print(f"Unrealized P/L:     ${profit_loss:.2f}")
    print(f"Return Percentage:  {return_percent:.2f}%")



def main():
    """
    Main program loop.
    """
    data = load_portfolio()

    while True:
        show_menu()
        choice = input("\nSelect an option: ").strip()

        if choice == "1":
            view_balance(data)
        elif choice == "2":
            log_buy(data)
        elif choice == "3":
            print("\nLog a sell feature coming soon.")
        elif choice == "4":
            view_open_positions(data)
        elif choice == "5":
            check_position_value(data)
        elif choice == "6":
            print("\nTrade history feature coming soon.")
        elif choice == "7":
            print("\nReset account feature coming soon.")
        elif choice == "0":
            print("]\nExiting Market Position Tracker.")
            break
        else:
            print("\nInvaild option. Please choose a vaild number.")


if __name__ == "__main__":
    main()