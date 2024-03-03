from CoreConnect import rpc
from CryptoConnect import getTopCrypto
import tkinter as tk
from datetime import datetime, timedelta
import threading

# Create the Tkinter window
root = tk.Tk()
root.title('Bitcoin Core Info')
root.geometry('1200x800')
root.configure(bg='black')

# Define global variables
start_time = datetime.now()
top_coins_available = []


# Functions to get information from RPC

def updateBlockCount(blockLabelUpdate):
    block_count = rpc('getblockcount')
    blockLabelUpdate.config(text=f'Block Count: {block_count}')
    blockLabelUpdate.after(10000, lambda: updateBlockCount(blockLabelUpdate))  # Update every 10 seconds
    return block_count


def getUptime(uptimeLabel):
    upTime = rpc('uptime')
    uptimeLabel.config(text=f'Server Uptime: {upTime}')
    uptimeLabel.after(300000, lambda: getUptime(uptimeLabel))  # Update every 5 minutes
    return upTime


def getBalance(balanceLabel):
    balance = rpc('getbalance')
    balanceLabel.config(text=f'Balance: {balance}')
    balanceLabel.after(3600000, lambda: getBalance(balanceLabel))  # Update every hour
    return balance


def getDifficulty(difficultyLabel):
    difficulty = rpc('getdifficulty')
    difficultyLabel.config(text=f'Difficulty: {difficulty}')
    difficultyLabel.after(60000, lambda: getDifficulty(difficultyLabel))  # Update difficulty every minute
    return difficulty


# Update coin information

def getTopCoins(topCoins):
    for coin in topCoins:
        name = coin["name"]
        currentPrice = coin["price"]
        top_coins_available.append({"name": name, "price": currentPrice})

    return top_coins_available


def displayTopCoin():
    global start_time

    # Clear previous labels
    for info in top_info_frame.winfo_children():
        info.destroy()

    # Update coin information
    def updateCoinInfo():
        top_coins = getTopCoins(getTopCrypto())
        for index, coin in enumerate(top_coins):
            coinLabel = tk.Label(top_info_frame, text=f'{coin["name"]}: ${coin["price"]}', fg='white', bg='black')
            coinLabel.grid(row=index, column=0, sticky='w', padx=10, pady=5)

    # Update refresh timer
    def refreshTimer():

        # Define lastRefresh label
        lastRefresh = tk.Label(top_info_frame, text='', fg='white', bg='black', anchor='w')
        lastRefresh.grid(row=len(top_coins_available) + 1, column=0)  # Place lastRefresh label below coins

        # Define refreshTimer label
        refreshTimerLabel = tk.Label(top_info_frame, text='', fg='white', bg='black', anchor='w')
        refreshTimerLabel.grid(row=len(top_coins_available) + 2, column=0)  # Place refreshTimer label below lastRefresh

        def updateRefreshLabel():
            global start_time

            # Update the time label to show the initial last updated time
            current_time = datetime.now().strftime("%H:%M:%S")
            lastRefresh.config(text=f"Last updated: {current_time}")

            # Update the time label every minute
            def refreshTime():
                global start_time
                remaining_time = (timedelta(seconds=300) - (datetime.now() - start_time)).seconds
                if remaining_time <= 0:
                    start_time = datetime.now()  # Reset the start time
                    remaining_time = 300  # Reset the remaining time to 5 minutes

                formatted_time = '{:02.0f}:{:02.0f}'.format(*divmod(remaining_time, 60))
                refreshTimerLabel.config(text=f"Next update in: {formatted_time}")
                root.after(1000, refreshTime)  # Update every second

            threading.Thread(target=refreshTime(), daemon=True)  # Initial call to refreshTime

        updateRefreshLabel()  # Initial call to updateRefreshLabel

        root.after(300000, lambda: displayTopCoin())  # Update top coins every 5 minutes

    updateCoinInfo()
    refreshTimer()  # Updated to top_info_frame


# Create a grid to hold all elements
root.grid_rowconfigure(len(top_coins_available), weight=1)
root.grid_columnconfigure(0)

# Frame for top coins and refresh timer
top_info_frame = tk.Frame(root, bg='black', highlightbackground="white", highlightthickness=1)
top_info_frame.grid(row=0, column=0, sticky='nw')  # Adjusted sticky to 'nsew'

# Frame for RPC info
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

bottom_info_frame = tk.Frame(root, bg='black', highlightbackground="white", highlightthickness=1)
bottom_info_frame.grid(row=2, column=0, stick='nw')

# Update the block count label
updateBlockLabel = tk.Label(bottom_info_frame, text='', fg='white', bg='black', highlightbackground="white",
                            highlightthickness=1)
updateBlockLabel.grid(row=0, column=0, padx=10, pady=5)

updateUptimeLabel = tk.Label(bottom_info_frame, text='', fg='blue', bg='black',
                             highlightbackground="white", highlightthickness=1)
updateUptimeLabel.grid(row=0, column=1, padx=10, pady=5)

updateBalanceLabel = tk.Label(bottom_info_frame, text='', fg='white', bg='black',
                              highlightbackground="white", highlightthickness=1)
updateBalanceLabel.grid(row=0, column=2, padx=10, pady=5)

updateDifficultyLabel = tk.Label(bottom_info_frame, text='', fg='blue', bg='black',
                                 highlightbackground="white", highlightthickness=1)
updateDifficultyLabel.grid(row=0, column=3, padx=10, pady=5)

# Start threads for updating information
threading.Thread(target=displayTopCoin, daemon=True).start()
threading.Thread(target=updateBlockCount, args=(updateBlockLabel,), daemon=True).start()
threading.Thread(target=getUptime, args=(updateUptimeLabel,), daemon=True).start()
threading.Thread(target=getBalance, args=(updateBalanceLabel,), daemon=True).start()
threading.Thread(target=getDifficulty, args=(updateDifficultyLabel,), daemon=True).start()

# Start the main loop
root.mainloop()
