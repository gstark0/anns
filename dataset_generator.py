import random
def xor(n, samples):
    for i in range(samples):
        x = random.uniform(-n, n)
        y = random.uniform(-n, n)
        
        if (y > 0 and x < 0) or (y < 0 and x > 0):
            label = 1
        else:
            label = -1
        f.write(str(x) + ',' + str(y) + ',' + str(label) + '\n')

with open('dataset.csv', 'w') as f:
    xor(6, 500)
