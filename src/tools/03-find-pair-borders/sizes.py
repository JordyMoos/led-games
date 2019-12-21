
# path the to pair file which is the file created by step `02-process-photos`
# for example
# PAIR_FILE = "./pair.csv"
PAIR_FILE = "../../../tutorials/01-introduction/tree-data/pair.csv"

'''

    End of configuration

'''

lines = [
    list(map(int, line.rstrip('\n').split(',', 3)))
    for line in open(PAIR_FILE)
]

xs = list(map(lambda line: line[1], lines))
ys = list(map(lambda line: line[2], lines))

print('x min = %d' % min(xs))
print('x max = %d' % max(xs))
print('')
print('y min %d' % min(ys))
print('y max %d' % max(ys))
