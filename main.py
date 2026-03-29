import yfinance as yf
import time
import matplotlib.pyplot as plt

stock = "BTC-USD"

balance = 10000
stocks_owned = 0
initial_balance = 10000

profit_history = []
plt.ion()

stocks = ["BTC-USD", "TSLA"]

stocks_owned = {s: 0 for s in stocks}
last_price = {s: 0 for s in stocks}

while True:
    for stock in stocks:
        data = yf.Ticker(stock)
        hist = data.history(period="100d")

        price = hist["Close"].iloc[-1]
        last_price[stock] = price 
        avg_price = hist["Close"].mean()

        print(f"\n--- {stock} ---")
        print(f"Price: {price}")
        print(f"Average Price: {avg_price}")

        # example logic
        if stocks_owned[stock] == 0:
            stocks_owned[stock] += 1
            print("BUY")

        else:
            stocks_owned[stock] -= 1
            print("SELL")

    

    # RSI calculation
    delta = hist["Close"].diff()

    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()

    rs = gain / loss.replace(0, 0.0001)
    rsi = 100 - (100 / (1 + rs))

    rsi = rsi.dropna()

    if len(rsi) == 0:
        print(" RSI not ready yet")
        time.sleep(5)
        continue

    current_rsi = rsi.iloc[-1]

    print("\n--- New Check ---")
    print(f"Price: {price}")
    print(f"Average Price: {avg_price}")
    print(f"RSI: {current_rsi}")

    action = "WAIT"

    # BUY
    if current_rsi < 40:
        print("📈 BUY Signal (RSI)")

        if balance >= price and stocks_owned == 0:
            stocks_owned += 1
            balance -= price
            print("✅ Bought 1 stock")

            with open("log.txt", "a") as f:
                f.write(f"BUY at {price} (RSI {current_rsi})\n")

    # SELL
    elif current_rsi > 60:
        print("📉 SELL Signal (RSI)")

        if stocks_owned > 0:
            stocks_owned -= 1
            balance += price
            print("✅ Sold 1 stock")

            with open("log.txt", "a") as f:
                f.write(f"SELL at {price} (RSI {current_rsi})\n")

    else:
        print("⏳ WAIT (RSI neutral)")

    # Net worth
    total_stock_value = 0

    for stock in stocks:
        total_stock_value += stocks_owned[stock] * last_price[stock]

    net_worth = balance + total_stock_value

    # Profit calculation
    profit = net_worth - initial_balance
    profit_history.append(profit)
    profit_percent = (profit / initial_balance) * 100

    plt.clf()  # clear previous graph
    plt.plot(profit_history)
    plt.title("Profit Over Time")
    plt.xlabel("Time")
    plt.ylabel("Profit")
    plt.pause(0.01)

    print(f"Balance: {balance}")
    print(f"Stocks Owned: {stocks_owned}")
    print(f" Net Worth: {net_worth}")
    print(f" Profit: {profit}")
    print(f" Profit %: {profit_percent:.2f}%")

    # Logging everything
    with open("log.txt", "a") as f:
        f.write(
            f"{action} | Price: {price} | RSI: {current_rsi:.2f} | "
            f"Balance: {balance} | Net Worth: {net_worth} | "
            f"Profit: {profit} ({profit_percent:.2f}%)\n"
        )
    

   
    time.sleep(5)