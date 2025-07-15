import sys
import pickle
import os


def load_pickle_file(filename):
    """Load data from a pickle file"""
    with open(filename, 'rb') as f:
        return pickle.load(f)


def save_pickle_file(filename, data):
    """Save data to a pickle file"""
    with open(filename, 'wb') as f:
        pickle.dump(data, f)


def clean_names(data_list):
    """Remove commas from Name field in the list"""
    return [item[:2] + [item[2].replace(',', '') if isinstance(item[2], str) else item[2]] + item[3:]
            for item in data_list]


def main():
    if len(sys.argv) != 2:
        print("Usage: python clean_commas.py <pickle_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = os.path.splitext(input_file)[0] + "_new" + os.path.splitext(input_file)[1]

    try:
        # Load data
        data = load_pickle_file(input_file)
        # Clean names
        cleaned_data = clean_names(data)
        # Save to new file
        save_pickle_file(output_file, cleaned_data)
    except Exception as e:
        print(f"Error processing file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
