#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 11:58:08 2023
Python code to take the report sent out by HUIT on SEAS Storage and produce an
extract that only contains the information we need. From that information, the
code also generates a report in .txt format on overall use, use for each of 
the various types of storage, and a listing of the top twenty users of each
type of storage, along with the amount of storage they use.

@author: waldo
"""

import sys, csv, pickle
import storage_summary as ss

# The fields to extract from the .csv file that is the full report from HUIT.
# note that the report has changed a couple of times, so this may change as well
#extract_list = [0,1,2,3,4,5,7,18,19,20,21,22,23] Extract list for April
extract_list = [0,1,2,3,4,5,7,16,17,18,19,20,21] #Extract list for May

#num_fields = {18,19,20,21,22,23} Numeric fields for April
num_fields = {16,17,18,19,20,21} #Numeric fields for May

# A dictionary of the fields in the extract list

data_dict = {'UUID': 0,
             'HUID': 1,
             'Name': 2,
             'Google_email': 3,
             'M365_Email': 4,
             'DB_email': 5,
             'Role': 6,
             'Google_store': 7,
             'Exchange_store': 8,
             'One_Drive_store': 9,
             'M365_store': 10,
             'Dropbox_store': 11,
             'total_store': 12
             }


def build_extract_list(from_iter, index_list):
    """
    Build a list of lists from the iterator from_iter, extracting the elements at the indices in index_list
    :param from_iter: An iterator that contains all the information sent by HUIT; this will generally be a csv.reader
    :param index_list: A list of the indices of the elements to be extracted; this will generally be extract_list but
    could change if the report from HUIT changes.
    :return: A list of lists with the extracted elements
    """
    extract = []
    for l in from_iter:
        e = []
        for i in index_list:
            if i in num_fields and not l[i].isalpha():
                e.append(convert_storage(l[i]))
            else:
                e.append(l[i])
        extract.append(e)
    return extract

def get_distribution(from_l,i):
    """
    Get the distribution of the values in the ith column of the list from_l, along with
    the total. It is assumed that the ith element is a storage amount, which is 0 if blank.
    The distribution will be number of accounts using less than 1GB, 1-10GB, 10-100GB, 100-1000GB,
    and over 1000GB
    :param from_l: A list that includes a field with storage use
    :param i: The field that contains the storage use
    :return: a total of stoage used and a 5-element list with the distribution
    """
    g_total = 0
    bins = [0,0,0,0,0]
    for l in from_l:
        tot = l[i]
        g_total += tot
        if tot < 1.0:
            bins[0] += 1
        elif tot < 10.0:
            bins[1] += 1
        elif tot < 100.0:
            bins[2] += 1
        elif tot < 1000.0:
            bins[3] += 1
        else:
            bins[4] += 1
            
    return g_total, bins

def get_id_list(from_l, id_index):
    """
    Get a list of the element of each list in from_l at index id_index
    :param from_l: A reduced list of storage use, which has the huid as the second element
    :return: a list of the HUIDs
    """
    return_l = []
    for l in from_l:
        return_l.append(l[id_index])
    return return_l

def convert_storage(amt_s):
    """
    Converts a storage amount from a string (from a .csv) to a float, with
    a space being interpreted as 0
    :param amt_s: A string representation of the amount of storage
    :return: a floating point representation of the amount of stor
    """
    if amt_s == '':
        ret_val = 0.0
    else:
        ret_val = float(amt_s)
    return ret_val


if __name__ == '__main__':
    """
    From the .csv file generated from the spreadsheet sent by HUIT, extract the fields we need and write them to a
    pickle file. Also generate a report on the storage use. The fields to be extracted are in extract_list, and the
    numeric fields are in num_fields. The fields are extracted in the order in which they appear in extract_list.
    Numeric fields are converted to floats, with a blank field being interpreted as 0.0.
    
    Command line arguments are the name of the .csv file and the name of the output file. The report is written to
    std.out, and so can be re-directed to a text file.
    """
    if len(sys.argv) < 3:
        print('Usage: python extractList.py storage_file.csv out_file.pkl')
        sys.exit(1)

    fin = open(sys.argv[1], 'r')
    cin = csv.reader(fin)

    fout = open(sys.argv[2], 'wb')
    h = next(cin)
    extract = build_extract_list(cin, extract_list)
    pickle.dump(extract, fout)

    fin.close()
    fout.close()

    print ("Total number of records: ", len(extract))
    print()

    total_storage = ss.Storage_Summary('Total', 12, extract)
    total_storage.print_summary()

    google_storage = ss.Storage_Summary('Google', 7, extract)
    google_storage.print_summary()
  
    db_store = ss.Storage_Summary('Dropbox', 11, extract)
    db_store.print_summary()

    exchange_storage = ss.Storage_Summary('Exchange', 8, extract)
    exchange_storage.print_summary()

    one_drive_storage = ss.Storage_Summary('One Drive', 9, extract)
    one_drive_storage.print_summary()
  

    sys.exit(0)