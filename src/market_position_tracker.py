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


def log_sell(data):
    """
    Sell an open position, calculate realized profit/loss,
    move it to trade history, and update balance.
    """
    print("\n--- Log a Sell ---")

    open_positions = data["open_positions"]

    if not open_positions:
        print("No open positions avaliable to sell.")
        return
    
    for index, position in enumerate(open_positions, start=1):
        print(f"{index}. {position['market_name']} ({position['side']})")

    try:
        selection = int(input("\nSelect a position number to sell: ").strip())
    except ValueError:
        print("\nInvaild selection. Please enter a number.")
        return
    
    if selection < 1 or selection > len(open_positions):
        print("\nSelected position does not exist.")
        return
    
    position = open_positions[selection - 1]

    try:
        sell_price = float(input("Enter sell price: ").strip())
    except ValueError:
        print("\nInvaild sell price entered.")
        return
    
    if sell_price <= 0 or sell_price >= 1:
        print("\nSell price must be greater than 0 and less than 1.")
        return
    
    sale_value = position["contracts"] * sell_price
    profit_loss = sale_value - position["amount_spent"]
    return_percent = (profit_loss / position["amount_spent"]) * 100

    closed_trade = {
        "market_name": position["market_name"],
        "side": position["side"],
        "entry_price": position["entry_price"],
        "sell_price": sell_price,
        "amount_spent": position["amount_spent"],
        "contracts": position["contracts"],
        "sale_value": sale_value,
        "profit_loss": profit_loss,
        "return_percent": return_percent,
        "status": "CLOSED"
    }

    data["current_balance"] += sale_value
    data["trade_history"].append(closed_trade)
    data["open_positions"].pop(selection - 1)
    save_portfolio(data)

    print("\nSell logged successfully.")
    print(f"Market:             {closed_trade['market_name']}")
    print(f"side:               {closed_trade['side']}")
    print(f"Entry Price:        ${closed_trade['entry_price']:.2f}")
    print(f"Sell Price:         ${closed_trade['sell_price']:.2f}")
    print(f"Amount Spent:       ${closed_trade['amount_spent']:.2f}")
    print(f"Sale Value:         ${closed_trade['sale_value']:.2f}")
    print(f"Realized P/L:       ${closed_trade['profit_loss']:.2f}")
    print(f"Return Percentage:  {closed_trade['return_percent']:.2f}%")
    print(f"New Balance:        ${data['current_balance']:.2f}")



def view_trade_history(data):
    """
    Display all closed trades from trade history.
    """
    print("\n--- Trade History ---")

    trade_history = data["trade_history"]

    if not trade_history:
        print("No closed trades found.")
        return
    
    for index, trade in enumerate(trade_history, start=1):
        print(f"\nTrade #{index}")
        print(f"Market:             {trade['market_name']}")
        print(f"Side:               {trade['side']}")
        print(f"Entry Price:        ${trade['entry_price']:.2f}")
        print(f"Sell Price:         ${trade['sell_price']:.2f}")
        print(f"Amount Spent:       ${trade['amount_spent']:.2f}")
        print(f"Contracts:          {trade['contracts']:.4f}")
        print(f"Sale Value:         ${trade['sale_value']:.2f}")
        print(f"Profit/Loss:        ${trade['profit_loss']:.2f}")
        print(f"Return Percentage:  {trade['return_percent']:.2f}%")
        print(f"Status:             {trade['status']}")


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
            log_sell(data)
        elif choice == "4":
            view_open_positions(data)
        elif choice == "5":
            check_position_value(data)
        elif choice == "6":
            view_trade_history(data)
        elif choice == "7":
            print("\nReset account feature coming soon.")
        elif choice == "0":
            print("]\nExiting Market Position Tracker.")
            break
        else:
            print("\nInvaild option. Please choose a vaild number.")


if __name__ == "__main__":
    main()