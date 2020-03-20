import time


class Timer:
    def __init__(self, gmt_offset):
        self.gmt = gmt_offset


obj = Timer(3)
obj2 = Timer




cur_time = time.time()

a = time.strptime('29 Jul 2015 23 39', '%d %b %Y %H %M')  # преобразовать строку в формат времени
b = time.mktime(a)
print('strptime: ', a)

print('epoch: {}'.format(b))
