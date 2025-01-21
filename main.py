import pyupbit


def main():
    print(pyupbit.get_current_price("KRW-BTC"))
    return True

if __name__ == '__main__':
    main()
