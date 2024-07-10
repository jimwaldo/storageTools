#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 17:09:05 2024

@author: jimwaldo

Find the difference between to lists stored in pickle files and generate a report. The lists will be
taken from the reports on who is using what storage from SEAS. The report will be in .csv format so that
we can use a spreadsheet as the user interface. The spreadsheet will contain entries for everyone that was
in the first file passed in as an argument who doesn't appear in the second file (which means they were
added) and for everyone in the second file who doesn't appear in the first file (which means they were removed).
The report will be in a file with the name passed in as the third argument.

"""

import pickle, sys, csv

def make_id_set(from_l):
    """
    Make a set from all of the UUIDs in the list of who is using storage. The UUIDs are the best way we have
    to identify the users. Note that entries that don't have a UUID will not be included.
    :param from_l: The list of users and how much storage they are using
    :return: A set of UUIDs for those users.
    """
    ret_s = set()
    for l in from_l:
        ret_s.add(l[0])
    return ret_s

def make_diff_list(diff_s, full_l):
    """
    Make a list of the entries in full_l that have a UUID in diff_s.
    :param diff_s: The set of UUIDs that we are looking for
    :param full_l: The list identified by UUIDs of full reports on the storage use
    :return: A list of the storage used by all users in diff_s
    """
    ret_l = []
    for l in full_l:
        if l[0] in diff_s:
            ret_l.append(l)
    return ret_l

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Usage: find_user_diffs.py file1.pkl file2.pkl diff_name')
        sys.exit(1)
        
    f1 = open(sys.argv[1], 'rb')
    list_1 = pickle.load(f1)
    f1.close()
    set_1 = make_id_set(list_1)
    
    f2 = open(sys.argv[2], 'rb')
    list_2 = pickle.load(f2)
    f2.close()
    set_2 = make_id_set(list_2)
    
    in_1_not_2 = set_1 - set_2
    in_2_not_1 = set_2 - set_1
    
    in_1_not_2_l = make_diff_list(in_1_not_2, list_1)
    in_2_not_1_l = make_diff_list(in_2_not_1, list_2)

    hin = open('header.pkl', 'rb')
    header = pickle.load(hin)
    hin.close()

    fout = open(sys.argv[3] + '.csv', 'w')
    cout = csv.writer(fout)
    cout.writerow(header)
    cout.writerow(['Accounts added between reports'])
    cout.writerows(in_1_not_2_l)

    cout.writerow([])
    cout.writerow(['Accounts removed between reports'])
    cout.writerows(in_2_not_1_l)

    fout.close()


