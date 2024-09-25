

# _codeathon_work.py
# sept 23, 2024





# codeathon work
desk = 'c:/users/hp/desktop/'
path = ''
file = 'xxx'



# 695 acinetobacter complete genome ids - for testing - 33 missing - ignore
file = 'acinetobacter_complete_genomes.txt'
genomes = []
for line in open(path + file, 'r'):
    genomes.append(line.strip())



# get plasmid coordinates



# corresponding AMR from isolate browser/MicroBIGG-E
# https://ncbi.nlm.nih.gov/pathogens/isolates#acinetobacter%20baumanii

# 36497, 5730 without GCA, 42 diplicate biosamples - GCA different - no error
# GCA#Bio
file = 'a_baumanii_36497_isolates.tsv'
n = 0; amrd = {}; amrc = 0
for line in open(path + file, 'r'):
    n = n + 1
    if n == 1: continue
    line = line.strip().split('\t') # len(line) == 16
    ID = line[14] + '#' + line[13]

    for amr in line[15].split(','):
        assert('=' in amr)
        amrc = amrc + 1
        amrd[amr] = amrd.get(amr, 0) + 1

# print(n, amrc, len(amrd))
# n=36498, amr=1152, amr#=570673

for k, v in amrd.items():
    # print(k, '\t', v)
    pass



# corresponding AST from AST browser
# https://ncbi.nlm.nih.gov/pathogens/ast/#acinetobacter%20baumanii

# 22064, 1131 unique biosamples (1132 PDT - 1 more - ignore)
file = 'a_baumanii_22064_asts.tsv'
n = 0; astd = {}
for line in open(path + file, 'r'):
    n = n + 1
    if n == 1: continue
    line = line.strip().split('\t') # len(line) == 17
    ID = line[0]
    drugc = line[7]+ '#' + line[8] + '#' + line[9] + '#' + line[10]
    astd[drugc] = astd.get(drugc, 0) + 1

print(n, len(astd))
# n=22064, astd=482

for k, v in astd.items():
    print(k, '\t', v)
    pass








