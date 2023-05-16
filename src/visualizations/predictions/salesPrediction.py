import matplotlib.pyplot as plt
import sys
import pickle
import os
import numpy as np
from numpy.polynomial import Polynomial as P
from dateutil.parser import parse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),'..' ,'..', '..', 'src', 'parsing')))
from DataReader import DataReader

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),'..', '..', '..', 'src', 'regression')))
from PolynomialRegression import PolynomialRegression

def main():

    reader = DataReader(os.path.join('dataset', 'dataSet.csv'))

    sales: list = reader.getAvgSalesPerDayInYear()
    function = sales
    degree: int = 40
    domain = range(len(sales))
    
    model = np.poly1d(np.polyfit(domain,function, degree))

    with open('dataset/sales_data.pkl', 'wb') as f:
        pickle.dump(sales, f)
    with open('dataset/model.pkl', 'wb') as f:
        pickle.dump(model, f)



    plotData(domain, function, model)
    
    
    
def plotData(domain, function, model):
    line = np.linspace(1, len(domain), len(domain))
    plt.plot(domain, function)
    plt.plot(line, model(line), color="red")
    plt.show()

if __name__ == "__main__":
    main()