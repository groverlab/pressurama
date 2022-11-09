import sys
with open(sys.argv[1], 'r') as fp:
    for count, line in enumerate(fp):
        pass
print('Total Lines', count + 1)
