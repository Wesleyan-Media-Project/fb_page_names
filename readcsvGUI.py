import pandas as pd
import argparse
import sys
from pandasgui import show

def parse_arguments():
    parser = argparse.ArgumentParser(description="Open a csv.gz file in a GUI for easy viewing and manipulation.")
    parser.add_argument('--file', type=str, required=True, help='Path to the CSV file.')
    return parser.parse_args()

def main():
    # Parse command-line arguments
    args = parse_arguments()
    
    file_path = args.file
    
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading data: {e}")
        sys.exit(1)
    
    # Launch GUI
    show(df)

if __name__ == "__main__":
    main()
