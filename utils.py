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
    sorted_df = df.sort_values(by='Value', ascending=False).reset_index()
    
    # Get the sorted keys from the index
    senders = sorted_df['Key'].tolist()
    counts = sorted_df['Value'].tolist()
    
    return dict(zip(senders, counts))