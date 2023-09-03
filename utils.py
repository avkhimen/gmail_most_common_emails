import pandas as pd

def increment_sender(sender_count, sender):
    if sender in sender_count:
        sender_count[sender] += 1
    else:
        sender_count[sender] = 1
    return sender_count

def sort_dict_by_values(dictionary):
    # Convert the dictionary to a DataFrame
    df = pd.DataFrame(dictionary.items(), columns=['Key', 'Value'])
    
    # Sort the DataFrame by 'Value' column in descending order
    sorted_df = df.sort_values(by='Value', ascending=False)
    
    # Get the sorted keys from the index
    sorted_keys = sorted_df['Key'].tolist()
    
    return sorted_keys