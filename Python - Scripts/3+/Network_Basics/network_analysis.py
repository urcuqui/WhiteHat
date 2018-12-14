"""
Author: Christian Camilo Urcuqui
Date: 14 december 2018
"""

# libraries
import netifaces


def main():
    nic_available()


def nic_available():
    netifaces.interfaces()


if __name__ == "__main__":
    main()
