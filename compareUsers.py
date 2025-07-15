import extractList
import pickle
import sys


def load_pickle_file(filename):
    """
    Load a pickle file containing user data
    """
    with open(filename, 'rb') as f:
        return pickle.load(f)


def find_unique_users(list1, list2):
    """
    Find users that exist in list1 but not in list2 and vice versa
    Returns two lists of tuples containing (HUID, Name) for unique users
    """
    users1 = {user[1]: user[2] for user in list1}
    users2 = {user[1]: user[2] for user in list2}

    unique_to_first = [(huid, name) for huid, name in users1.items() if huid not in users2]
    unique_to_second = [(huid, name) for huid, name in users2.items() if huid not in users1]

    return unique_to_first, unique_to_second


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python compareUsers.py first_file.pkl second_file.pkl')
        sys.exit(1)

    first_list = load_pickle_file(sys.argv[1])
    second_list = load_pickle_file(sys.argv[2])

    unique_first, unique_second = find_unique_users(first_list, second_list)

    print("\nUsers in first file but not in second:")
    for huid, name in unique_first:
        print(f"HUID: {huid}, Name: {name}")
    print (f"\nTotal unique users in first file: {len(unique_first)}")

    print("\nUsers in second file but not in first:")
    for huid, name in unique_second:
        print(f"HUID: {huid}, Name: {name}")
    print (f"\nTotal unique users in second file: {len(unique_second)}")