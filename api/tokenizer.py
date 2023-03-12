import csv
import transformers

# Load the GPT-2 tokenizer
tokenizer = transformers.GPT2Tokenizer.from_pretrained('gpt2')

# Open the CSV file for reading
with open('dataset.csv','r',encoding="cp1252") as file:
    # Create a reader object
    reader = csv.reader(file)
        
    # Read the header row
    header = next(reader)
        
    # Add a new header "tokens" to the header row
    header.append("tokens")
        
    # Open a new CSV file for writing
    with open('dataset_tokens.csv', 'w', newline='') as file_tokens:
        # Create a writer object
        writer = csv.writer(file_tokens)
            
        # Write the header row to the new CSV file
        writer.writerow(header)
            
        # Loop over the rows in the original CSV file
        for row in reader:
            # Tokenize the "heading" and "content" columns
            heading_tokens = tokenizer.tokenize(row[1])
            content_tokens = tokenizer.tokenize(row[2])
                
            # Count the number of tokens in the "heading" and "content" columns
            heading_token_count = len(heading_tokens)
            content_token_count = len(content_tokens)
                
            # Calculate the total number of tokens
            total_token_count = heading_token_count + content_token_count
                
            # Add the total number of tokens to the row
            row.append(total_token_count)
                
            # Write the row to the new CSV file
            writer.writerow(row)