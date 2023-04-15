import csv
import tiktoken

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    #encoding = tiktoken.get_encoding(encoding_name)
    encoding = tiktoken.encoding_for_model(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

#print(num_tokens_from_string("Your text string goes here", "text-embedding-ada-002"))

# Open the CSV file for reading
def tokenize():
    with open('dataset/concatenated_dataset.csv','r',encoding="cp1252") as file:
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
                heading_tokens = num_tokens_from_string(row[1], "text-davinci-003")
                content_tokens = num_tokens_from_string(row[2], "text-davinci-003")
                    
                # Calculate the total number of tokens
                total_token_count = heading_tokens + content_tokens
                    
                # Add the total number of tokens to the row
                row.append(total_token_count)
                    
                # Write the row to the new CSV file
                writer.writerow(row)