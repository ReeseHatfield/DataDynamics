import matplotlib.pyplot as plt
import sys
import pickle
import os
import numpy as np

from src.parsing.DataReader import DataReader


def main():
    # Load data from file if it exists, otherwise compute it
    sales, model = load_or_compute_data()

    # Plot the data
    plot_data(range(len(sales)), sales, model)


def load_or_compute_data():
    data_file = os.path.join("data", 'serialized', "sales_data.pkl")
    model_file = os.path.join("data", 'serialized', "model.pkl")

    if os.path.exists(data_file) and os.path.exists(model_file):
        print("Using pre-computed data")
        # Load data from file
        with open(data_file, 'rb') as f:
            sales = pickle.load(f)
        with open(model_file, 'rb') as f:
            model = pickle.load(f)
    else:
        print("Computing data")
        # Compute data
        reader = DataReader(os.path.join('data', 'dataSet.csv'))
        sales = reader.get_avg_sales_per_day_in_year()
        degree: int = 40
        domain = range(len(sales))
        model = np.poly1d(np.polyfit(domain, sales, degree))

        # Save data to file
        with open(data_file, 'wb') as f:
            pickle.dump(sales, f)
        with open(model_file, 'wb') as f:
            pickle.dump(model, f)

    return sales, model


def plot_data(ax, domain, function, model, eval_pos=None):
    line = np.linspace(1, len(domain), len(domain))
    ax.plot(domain, function)
    ax.plot(line, model(line), color="red")

    if eval_pos is not None:
        ax.axvline(x=eval_pos, color='black', label='Predicted Line', linewidth=4)

    return ax


if __name__ == '__main__':
    main()
