import os
path = 'test/'
counter = 1
for f in os.listdir(path):
    new = '{}.{}'.format(str(counter), 'jpeg')
    os.rename(path + f, path + new)
    counter = int(counter) + 1
