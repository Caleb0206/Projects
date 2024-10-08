input = open('dictionary_a-c.txt', 'r')
out = open('dictionary_a-c_new.txt', 'w')

for line in input:
    s = line.strip()
    out.write(s + '\n')