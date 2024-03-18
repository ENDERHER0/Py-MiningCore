import CryptoCSV as ccsv
import sys
from time import sleep
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
import pandas as pd
import pylab as pl
import numpy as np
import os
import threading

np.set_printoptions(threshold=sys.maxsize)

filePath = "StockData/stocks.csv"


def build_linear_regression_model():
    df = pd.read_csv(filePath)

    # Drop any rows with missing values
    df.dropna(inplace=True)

    # Convert Date column to datetime format with specified format
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d %H.%M.%S')

    # Extract date features
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Day'] = df['Date'].dt.day

    # Sort DataFrame by Date
    df.sort_values(by='Date', inplace=True)

    # Set Date column as the index
    df.set_index('Date', inplace=True)

    # Define features and target
    trainingFeatures = ["Ethereum", "BNB", "XRP", "Dogecoin", "Year", "Month", "Day"]

    target = ["Bitcoin"]

    # Extract features and target
    features = df[trainingFeatures]
    target = df[target]

    # Set up a mask to split the dataset into training and testing sets
    # Use the last portion of data as the test set for predicting future prices
    test_size = 0.2
    split_index = int(len(df) * (1 - test_size))

    X_train = features.iloc[:split_index]
    y_train = target.iloc[:split_index]
    X_test = features.iloc[split_index:]
    y_test = target.iloc[split_index:]

    # Building the model
    regression = linear_model.LinearRegression(fit_intercept=False)
    regression.fit(X_train, y_train)

    # Coefficients
    print('Coefficients: ', regression.coef_)

    # Predictions
    y_hat = regression.predict(X_test)

    # Calculate MSE and R-squared
    mse = mean_squared_error(y_test, y_hat)
    print("Mean Squared Error (MSE):", mse)

    r_squared = r2_score(y_test, y_hat)
    print("R-squared score:", r_squared)

    # Print out the predicted Bitcoin price
    predicted_price = y_hat[-1][0]
    print("Predicted Bitcoin Price:", predicted_price)

    # Get the actual Bitcoin price for the next time step
    next_actual_price = target.iloc[split_index].values[0]
    print("Next Actual Bitcoin Price:", next_actual_price)

    # Determine if the next actual price is higher or lower than the predicted price
    if next_actual_price > predicted_price:
        print("Next Actual Price is higher than the Predicted Price")
    elif next_actual_price < predicted_price:
        print("Next Actual Price is lower than the Predicted Price")
    else:
        print("Next Actual Price is the same as the Predicted Price")

    def plot_predictions(y_test, y_hat):
        """
        Plot predictions.

        Args:
        - y_test (pandas.Series): Series containing the actual Bitcoin prices.
        - y_hat (numpy.ndarray): Numpy array containing the predicted Bitcoin prices.

        Returns:
        None
        """
        print("Plotting predictions.")
        # Increase the number of data points by selecting a larger portion of the dataset
        # For example, you can select the last 100 data points
        num_data_points = 100
        y_test_subset = y_test[-num_data_points:]
        y_hat_subset = y_hat[-num_data_points:]

        if plt.fignum_exists(1):
            plt.figure(1)
            plt.clf()

        plt.figure(1, figsize=(10, 6))
        plt.plot(y_test_subset.index, y_test_subset, label='Actual Bitcoin Price', drawstyle='steps-mid')
        plt.plot(y_test_subset.index, y_hat_subset, label='Predicted Bitcoin Price', drawstyle='steps-pre')
        plt.xlabel('Date')
        plt.ylabel('Bitcoin Price')
        plt.title('Bitcoin Price Prediction')
        plt.legend()
        plt.show(block=False)
        print("New window plotted")

    threading.Thread(target=plot_predictions(y_test, y_hat), daemon=True).start()


def updateModel():
    running = True
    while running:
        # Execute building linear regression model on the main thread
        build_linear_regression_model()

        # Start thread for updating CSV file
        csv_thread = threading.Thread(target=ccsv.update_crypto_csv, args=(filePath,))
        csv_thread.start()

        # Wait for the CSV update to complete before proceeding
        csv_thread.join()

        # Start thread for sleeping
        sleep_thread = threading.Thread(target=sleep, args=(150,))
        sleep_thread.start()


# Start the updateModel function in a separate thread
updateModel()

# Main thread continues execution
# You can add more code here if needed
