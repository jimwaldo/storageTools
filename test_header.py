#!/usr/bin/evn python3
# -*- coding: utf-8 -*-
"""
Created on 5/14/24
Quick check to insure that the csv file obtained from HUIT has the same columns in the same order as the standard, which
is the assumed order for the rest of the programs.
@author waldo

"""
import pickle, csv, sys

def check_headers(h_1, h_2):
    ret_v = True
    if h_1 != h_2:
        ret_v = False
        if len(h_1) != len(h_2):
            print ('Headers of of different length')
            return False
        for i in range(0, len(h_1)):
            if h_1[i] != h_2[i]:
                print (h_1[i], h_2[i])
    return ret_v

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: test_header.py standard_file.pkl test_file.csv")
        sys.exit(1)

    fin = open(sys.argv[1], 'rb')
    standard = pickle.load(fin)
    fin.close()

    fin = open(sys.argv[2], 'r')
    cin = csv.reader(fin)
    test_h = next(cin)
    fin.close()

    if check_headers(standard, test_h):
        print("Headers are the same")

    sys.exit(0)
