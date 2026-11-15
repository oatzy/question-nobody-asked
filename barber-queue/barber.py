import logging
from math import exp
from numpy.random import poisson
from random import random, randint
from uuid import uuid4

logging.basicConfig(
    format='%(message)s',
    level=logging.WARN
)


# arrival rate
ARATE = 0.7
# number of workers
WORKERS = 2
# waiting area capacity
CAPACITY = 10


class BarberQueue(object):

    class Member(object):

        def __init__(self, obj, position=0):
            self.value = obj
            self._position = position

        def __str__(self):
            return "%s (%s)" % (self.value, self._position)

        def is_next(self):
            return self._position == 0

        def is_behind(self, other):
            return self._position > other._position

        def move_up(self):
            self._position -= 1

    def __init__(self, capacity):
        self._capacity = capacity
        self._queue = [None]*capacity
        self._length = 0

    def __len__(self):
        return self._length

    def __str__(self):
        return ', '.join(str(i) if i is not None else '_'
                         for i in self._queue)

    def push(self, obj):

        if self._length >= self._capacity:
            if obj.will_wait(self._length, self._capacity):
                self._queue.append(BarberQueue.Member(obj, self._length))
                self._length += 1
                logging.info("%s joined the queue", obj)
            else:
                logging.warn("%s wasn't added to the queue", obj)
            return

        for i, m in enumerate(self._queue):
            if m is None:
                self._queue[i] = BarberQueue.Member(obj, self._length)
                self._length += 1
                logging.info("%s joined the queue", obj)
                return

    def pop(self):
        value = None

        for i, m in enumerate(self._queue):
            if m is not None:
                if m.is_next():
                    value = m.value
                    self._queue[i] = None
                    self._length -= 1
                else:
                    m.move_up()
        return value

    def _remove(self, member):
        for i, m in enumerate(self._queue):
            if m == member:
                self._queue[i] = None
                self._length -= 1
            elif m is not None and m.is_behind(member):
                m.move_up()

    def update(self):
        for m in self._queue:
            if m is not None:
                m.value.update()
                if m.value.will_leave(m._position):
                    logging.warn("%s left after %s",
                                 m.value.name, m.value._wait)
                    self._remove(m)
        # TODO: if 'seats' are avaiable and
        # people are 'standing', move them to seats


class Person(object):

    def __init__(self, name):
        self.name = name
        self.cut_duration = randint(2, 5)
        self._wait = 0.

    def __str__(self):
        return str(self.name)

    def will_wait(self, length, capacity):
        return random() >= 0.25*length/capacity

    def will_leave(self, position, sunk=False):
        if position == 0:
            return 0
        if sunk:
            return random() < 0.05*exp(-self._wait/position)
        else:
            return random() < 0.01*exp(-5./(self._wait*position))

    def update(self):
        self._wait += 1


class Worker(object):

    def __init__(self):
        self._customer = None
        self._duration = 0

    def cut_hair(self, customer):
        logging.info("%s waited %s",
                     customer.name, customer._wait)
        self._customer = customer
        self._duration = 1

    def is_free(self):
        return self._customer is None

    def update(self):
        if self._customer is None:
            return
        if self._duration == self._customer.cut_duration:
            self._customer = None
            self._duration = 0
        else:
            self._duration += 1


class BarberShop(object):

    def __init__(self, workers, capacity):
        self._workers = [Worker()] * workers
        self._queue = BarberQueue(capacity)

    def update(self, new_customers=None):

        # check if anyone wants to leave
        self._queue.update()

        # add any new customers to the queue
        if new_customers:
            for c in new_customers:
                self._queue.push(c)

        # check if works have finished hair cutting
        for w in self._workers:
            w.update()
            if w.is_free():
                nxt = self._queue.pop()
                if nxt is not None:
                    w.cut_hair(nxt)

        # print self._queue

        return len(self._queue)


def main(steps):
    b = BarberShop(WORKERS, CAPACITY)

    # 1 step = 5 mins
    for t in xrange(steps):

        # how many people arrived this interval?
        arrivals = poisson(ARATE)

        # each person is given a random uuid as a name
        q_size = b.update([Person(str(uuid4()).split('-')[0])
                           for _ in xrange(arrivals)])

        print t, q_size

    # closing time - continue until empty queue
    while q_size > 0:

        t += 1
        q_size = b.update()

        print t, q_size


if __name__ == '__main__':
    main(48)  # 4 hours
