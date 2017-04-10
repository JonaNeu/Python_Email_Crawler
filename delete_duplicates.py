with open('emails.csv','r') as in_file, open('emails_2.csv','w') as out_file:
    seen = set()
    for line in in_file:
        if line not in seen:
            seen.add(line)
            out_file.write(line)