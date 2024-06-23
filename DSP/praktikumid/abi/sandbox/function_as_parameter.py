#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import time


def print_hello_world():
    print("Hello world")


def calculate_sum_of_first_10000000_numbers():
    result = 0
    for i in range(1, 10000001):
        result += i
    return result


def time_function(measurable):
    start = time.time()
    measurable()
    end = time.time()
    return end - start


def main():
    time1 = time_function(print_hello_world)
    time2 = time_function(calculate_sum_of_first_10000000_numbers)

    print(f"Funktsioon 'print_hello_world' võttis {time1} sekundit")
    print(f"Funktsioon 'calculate_sum_of_first_10000000_numbers' võttis {time2} sekundit")


if __name__ == "__main__":
    main()
