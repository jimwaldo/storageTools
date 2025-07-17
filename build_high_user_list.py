#!/usr/bin/env python3
"""Created on Fri Oct 27 11:58:08 2023
Python code to take the report sent out by HUIT on SEAS Storage and produce an
extract that contains the name, email, role, and storage value for the top 20 users
of a specified storage type. The code generates a CSV file with this information.
"""


import csv
import sys
import pickle


def get_top_20_users(data_list, field_index):
    """
    Sort and return top 20 users based on specified field
    """
    sorted_list = sorted(data_list, key=lambda x: float(x[field_index]) if x[field_index] != '' else 0.0, reverse=True)
    return sorted_list[:20]


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Usage: python build_high_user_list.py input.pkl output.csv field_index')
        sys.exit(1)

    try:
        with open(sys.argv[1], 'rb') as fin:
            data = pickle.load(fin)

        field_index = int(sys.argv[3])
        top_users = get_top_20_users(data, field_index)

        out_list = []

        out_list.append(["Top 20 users by field index {field_index}".format(field_index=field_index)])
        out_list.append(['Name', 'Email', 'Role','Storage Value'])
        for user in top_users:
            out_list.append([user[2], user[3], user[6], user[field_index]])
        with open(sys.argv[2], 'w', encoding='utf-8') as fout:
            cout = csv.writer(fout)
            cout.writerows(out_list)

    except FileNotFoundError:
        print(f"Error: File {sys.argv[1]} not found")
        sys.exit(1)
    except ValueError:
        print("Error: Field index must be a valid integer")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
