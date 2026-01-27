import matplotlib.pyplot as plt
import numpy as np
import argparse
from utils import compute_errors, read_axis_from_file, draw, save_thetas

def gradient_descent(x_scaled, y_scaled):
    MAX_STEPS = 1000
    MIN_GRAD_MAGNITUDE = 1e-4
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

def clean_and_verify_arrays(x, y):
    x = x[~np.isnan(x)]
    y = y[~np.isnan(y)]
    if (len(x) != len(y)):
        print("There is an issue with the data please verify")
        exit(1)
    return x, y


def main():
    parser = argparse.ArgumentParser(description="Compute a linear regression")
    parser.add_argument("-d", "--draw", action="store_true", help="draw the plotted data")
    parser.add_argument("-s", "--save", action="store_true", help="save the image")
    parser.add_argument("-v", "--verify",  action="store_true", help="Compare the gradient descent to the analytic solution")
    args = parser.parse_args()

    x_original, y_original = read_axis_from_file("data.csv")
    x_original, y_original = clean_and_verify_arrays(x_original, y_original)


    theta0, theta1 = linear_regression(x_original,y_original)
    save_thetas(theta0, theta1)
    draw(theta0, theta1, x_original, y_original, args.draw, args.save)

    if (args.verify):
        percent_error, absolute_error, T, E = compute_errors()
        print(f"Set E = {T} (gradient descent) and T = {E} (analytic solution)")
        print(f"Absolute error: |E - T| = {absolute_error:.4f}")
        print(f"Percent error: |abs_error/|T| | x 100 = {percent_error:.2f}%")

if __name__ == "__main__":
    main()
