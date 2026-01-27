def read_thetas():
    try:
        f = open("thetas.csv", "r")
        thetas = f.readline().split(',')
        thetas = [float(theta) for theta in thetas]
        f.close()
    except Exception:
        return [0, 0]
    return thetas

def price_estimation(thetas, mileage):
    if (mileage < 0):
        raise Exception("Mileage must be positive")
    return thetas[0] + thetas[1] * mileage


def main():
    try:
        mileage = input("Please enter a mileage :\n")
        thetas = read_thetas()
        print(f"This car is worth {price_estimation(thetas, float(mileage)):.2f}€")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()
