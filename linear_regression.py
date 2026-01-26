import matplotlib.pyplot as plt
import numpy as np
import sys

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

def gradient_descent(x_scaled, y_scaled):
    MAX_STEPS = 1000
    MIN_GRAD_MAGNITUDE = 1e-6
    LEARNING_RATE = 0.01
    theta0, theta1 = 0.0, 0.0
    m = len(x_scaled)

    for _ in range(MAX_STEPS):
        estimation = theta0 + theta1 * x_scaled
        error = estimation - y_scaled

        tmp_theta0 = LEARNING_RATE * 1/m * np.sum(error)
        tmp_theta1 = LEARNING_RATE * 1/m * np.sum(error * x_scaled)

        if abs(tmp_theta0) < MIN_GRAD_MAGNITUDE and abs(tmp_theta1) < MIN_GRAD_MAGNITUDE:
            break;
        theta0, theta1 = theta0 - tmp_theta0, theta1 - tmp_theta1
    return theta0, theta1

def linear_regression(x_original, y_original):
    mean_x = np.mean(x_original)
    std_x = np.std(x_original)
    x_scaled = (x_original - mean_x) / std_x

    mean_y = np.mean(y_original)
    std_y = np.std(y_original)
    y_scaled = (y_original - mean_y) / std_y
    theta0_scaled, theta1_scaled = gradient_descent(x_scaled,y_scaled)
    theta1 = theta1_scaled * (std_y / std_x)
    theta0 = theta0_scaled * std_y + mean_y - theta1 * mean_x

    return theta0, theta1

def main():
    drawing = False
    verify = False
    args = sys.argv[1:]
    if (len(args) == 1):
        if(args[0] == "--draw" or args[0] == "-d"):
            drawing = True
        else:
            print("Option(s):\t--draw (-d)")
            print("\t\t--verify (-v)")
            exit(1)
    x_original, y_original = read_axis_from_file("data.csv")


    theta0, theta1 = linear_regression(x_original,y_original)
    print(f"{theta0}, {theta1}")
    save_data(theta0, theta1)
    draw(theta0, theta1, x_original, y_original, drawing)
    verfiy(theta0, theta1, x_original, y_original, verify)

if __name__ == "__main__":
    main()

def verfiy(theta0_gradient, theta1_gradient, x, y, draw=False, verify=True):
    if not verify:
        return
    # TODO: calculate precise values and compare to theta0 and theta1
    pass

def draw(theta0, theta1, x, y, draw=False, save=True):
    plt.figure()
    plt.grid()
    plt.title("Price estimation with respect to mileage")
    plt.xlabel("mileage [km]")
    plt.ylabel("price [€]")
    plt.scatter(x, y, color = 'black', marker='+', label='Data')

    x_space = np.linspace(np.min(x), np.max(x))
    y_x = theta0 + theta1 * x_space
    plt.plot(x_space, y_x, color='red',  label=f"y = {theta1:.2f}x + {theta0:.2f}")

    plt.legend()
    if save:
        plt.savefig("fig")
        print(f"Image was successfully created")
    if draw:
        plt.show()

def save_data(theta0, theta1, namefile="thetas.csv"):
    try:
        with open(namefile, "w", encoding="utf-8") as f:
            f.write(f"{theta0},{theta1}")
            print(f"File {namefile} was successfully created")
    except Exception as e:
        print(f"Error: {e}")


