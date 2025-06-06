import csv

# Path to the CSV file
csv_file = "data/ShailosophyQuotes.csv"

# Read and print the first 5 rows
try:
    with open(csv_file, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        
        # Print the first 5 rows
        print("First 5 quotes:")
        for i, row in enumerate(csv_reader):
            if i < 5:
                print(f"ID: {row[0]}, Quote: {row[1]}")
            else:
                break
        
        # Count total quotes
        file.seek(0)  # Reset file pointer
        quote_count = sum(1 for _ in csv_reader)
        print(f"\nTotal quotes: {quote_count}")
        
except Exception as e:
    print(f"Error: {e}") 