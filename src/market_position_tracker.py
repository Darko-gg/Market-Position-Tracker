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
            print("\nLog a buy feature coming soon.")
        elif choice == "3":
            print("\nLog a sell feature coming soon.")
        elif choice == "4":
            print("\nView open positions feature coming soon.")
        elif choice == "5":
            print("\nPosition value checker feature coming soon.")
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