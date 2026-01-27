import numpy as np
import matplotlib.pyplot as plt
from price_estimation import read_thetas

def read_axis_from_file(path):
    try:
        data = np.genfromtxt(path, delimiter = ',', skip_header=1)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
    if (len(data) == 0 or len(data[0]) == 0 or len(data[:,0]) == 0):
        print(f"Error with the data file");
        exit(1)
    x = data[:,0].copy()
    y = data[:,1].copy()
    if not (len(data) == len(x) == len(y)):
        print(f"Error with the data file");
        exit(1)
    return x,y

def draw(theta0, theta1, x, y, draw=False, save=False):
    plt.figure(num="data points")
    plt.grid()
    plt.title("Price estimation with respect to mileage")
    plt.xlabel("mileage [km]")
    plt.ylabel("price [€]")
    plt.scatter(x, y, color = 'black', marker='+', label='Data')

    plt.figure(num="data and linear fit")
    plt.grid()
    plt.title("Price estimation with respect to mileage with linear fit")
    plt.xlabel("mileage [km]")
    plt.ylabel("price [€]")
    plt.scatter(x, y, color = 'black', marker='+', label='Data')
    x_space = np.linspace(np.min(x), np.max(x))
    y_x = theta0 + theta1 * x_space
    plt.plot(x_space, y_x, color='red',  label=f"y = {theta1:.2f}x + {theta0:.2f}")

    plt.legend()
    if save:
        plt.figure(num="data points")
        plt.savefig("data_only.png")
        plt.figure(num="data and linear fit")
        plt.savefig("data_with_line.png")
        print(f"Images saved")
    if draw:
        plt.show()

def save_thetas(theta0, theta1, namefile="thetas.csv"):
    try:
        with open(namefile, "w", encoding="utf-8") as f:
            f.write(f"{theta0},{theta1}")
            print(f"File {namefile} was successfully created")
    except Exception as e:
        print(f"Error: {e}")

def compute_theoretical(path = "data.csv"):
    x, y = read_axis_from_file(path)
    size = len(x)
    theta1 = (np.sum(x*y) - (np.sum(x) * np.sum(y)) / size) / (np.sum(x*x) - (np.sum(x)**2)/size)

    theta0 = (np.sum(y) - theta1 * np.sum(x)) / size
    return theta0, theta1

# E: experimantal
# T: theoretical
def compute_errors():
    theoretical_theta0, theoretical_theta1 = compute_theoretical()
    thetas = read_thetas()
    T = np.array([theoretical_theta0, theoretical_theta1])
    E = np.array(thetas)
    diff = E - T
    absolute_error = np.linalg.norm(diff)
    T_mag = np.linalg.norm(T)
    percent_error = (absolute_error / T_mag) * 100
    return percent_error, absolute_error, T, E
