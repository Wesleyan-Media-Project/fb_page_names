import pandas as pd
import datetime
import argparse
import os

# Constants
CHUNK_SIZE = 1048570    
# Number of rows per chunk for maximum number of rows Excel can handle. 
# The offical limit is 1048576, but we use a slightly smaller number just for safe.

# Set up argument parsing
def parse_arguments():
    parser = argparse.ArgumentParser(description="Filter large CSV files and save results to multiple Excel files if necessary.")
    parser.add_argument('--file', type=str, required=True, help='Path to the CSV file.')
    parser.add_argument('--skiprows', type=int, default=0, help='Number of rows to skip at the start of the file.')
    parser.add_argument('--nrows', type=int, default=10000, help='Number of rows to read from the file. Read 10000 rows if not specified.')
    parser.add_argument('--filter_text', type=str, default='', help='Text to filter the rows.')
    return parser.parse_args()

def load_data(file_path, skiprows, nrows):
    # Load data from the CSV file with specified rows to skip and number of rows to read
    try:
        df = pd.read_csv(file_path, skiprows=skiprows, nrows=nrows)
        if nrows is not None and df.shape[0] < nrows:
            print(f"Warning: This data has only {df.shape[0]} rows and is less than the requested {nrows} rows. The script will read all rows in the data in this case.")
        return df
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        exit(1)
    except Exception as e:
        print(f"Error loading data: {e}")
        exit(1)

def filter_data(df, text):
    # Filter the DataFrame based on the provided text
    return df[df.apply(lambda row: row.astype(str).str.contains(text, case=False, na=False).any(), axis=1)]

def save_to_excel(df, file_prefix='Readcsvgz_Output'):
    # Save the DataFrame to multiple Excel files if it exceeds the row limit
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    if df.shape[0] <= CHUNK_SIZE:
        excel_file_path = f'{file_prefix}_{timestamp}.xlsx'
        try:
            df.to_excel(excel_file_path, index=False)
            print(f"Filtered data saved to: {excel_file_path}")
        except Exception as e:
            print(f"Error saving to Excel: {e}")
    else:
        num_chunks = (df.shape[0] // CHUNK_SIZE) + 1
        for i in range(num_chunks):
            start_row = i * CHUNK_SIZE
            end_row = min(start_row + CHUNK_SIZE, df.shape[0])
            chunk = df.iloc[start_row:end_row]
            excel_file_path = f'{file_prefix}_{timestamp}_part{i+1}.xlsx'
            try:
                chunk.to_excel(excel_file_path, index=False)
                print(f"Filtered data saved to: {excel_file_path}")
            except Exception as e:
                print(f"Error saving to Excel: {e}")

def main():
    # Parse command-line arguments
    args = parse_arguments()
    
    # Output the entered options
    skiprows_desc = args.skiprows
    nrows_desc =  args.nrows
    filter_text_desc = "No filter is applied" if args.filter_text == '' else args.filter_text
    
    print(f"Input file: {args.file}")
    print(f"Start reading data from row: {skiprows_desc}")
    print(f"Number of rows to read: {nrows_desc}")
    print(f"Filter text: {filter_text_desc}")
    
    if args.nrows and args.nrows > CHUNK_SIZE:
        print(f"Note: The requested data will be stored into multiple Excel due to the maximum number of rows (1048576) Excel can handle.")
    
    df = load_data(args.file, args.skiprows, args.nrows)
    filtered_df = filter_data(df, args.filter_text)
    
    # Set display options to avoid truncation in columns
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_rows', None)
    save_to_excel(filtered_df)

if __name__ == "__main__":
    main()