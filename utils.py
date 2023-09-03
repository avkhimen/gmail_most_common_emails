def increment_sender(sender_count, sender):
    if sender in sender_count:
        sender_count[sender] += 1
    else:
        sender_count[sender] = 1
    return sender_count