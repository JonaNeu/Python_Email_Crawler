import re
from validate_email import validate_email


with open('emails.csv','r', encoding="latin-1") as in_file, open('emails_2.csv','w') as out_file:
    seen = set()
    for line in in_file:
        if re.match(r'[^@]+@[^@]+\.[^@]+', line) and not line.startswith("cached") and not line[-1:] == ".":
            if line not in seen:
                if validate_email(line):
                    seen.add(line)
                    out_file.write(line)
            if line.endswith(".") and line[:-1] not in seen:
                if validate_email(line):
                    seen.add(line)
                    out_file.write(line)