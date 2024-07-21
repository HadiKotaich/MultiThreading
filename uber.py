from threading import Condition, Lock, current_thread, Thread
import random

class Uber:
    def __init__(self):
        self.democrats_count = 0
        self.republicans_count = 0
        self.lock = Lock()
        self.condition = Condition()
        self.ride_count = 0
        self.choice = [] #4 0, 2 2, 0 4

    def drive(self):
        self.ride_count += 1
        print("Uber ride # {0} filled and on its way".format(self.ride_count))

    def seated(self, party):
        print("\n{0} {1} seated".format(party, current_thread().name))

    def seat_democrat(self):
        with self.condition:
            self.democrats_count += 1
            self.condition.wait_for(lambda:
                    (len(self.choice) == 0 and (self.democrats_count >= 4 or self.republicans_count >= 2 and self.democrats_count >= 2))
                    or (len(self.choice) > 0 and self.choice[0] > 0))
            if len(self.choice) == 0:
                if self.democrats_count >= 4:
                    self.choice = [4, 0]
                else:
                    self.choice = [2, 2]
            self.democrats_count -= 1
            self.choice[0] -= 1
            self.seated("democrat")
            if self.choice == [0, 0]:
                self.drive()
                self.choice = []
            self.condition.notify_all()

    def seat_republican(self):
        with self.condition:
            self.republicans_count += 1
            self.condition.wait_for(lambda:
                    (len(self.choice) == 0 and (self.republicans_count >= 4 or self.republicans_count >= 2 and self.democrats_count >= 2))
                    or (len(self.choice) > 0 and self.choice[1] > 0))
            if len(self.choice) == 0:
                if self.republicans_count >= 4:
                    self.choice = [0, 4]
                else:
                    self.choice = [2, 2]
            self.republicans_count -= 1
            self.choice[1] -= 1
            self.seated("repub")
            if self.choice == [0, 0]:
                self.drive()
                self.choice = []
            self.condition.notify_all()



problem = Uber()
dems = 10
repubs = 10

total = dems + repubs
print("Total {0} dems and {1} repubs\n".format(dems, repubs))

riders = list()

while total != 0:
    toss = random.randint(0, 1)
    if toss == 1 and dems != 0:
        riders.append(Thread(target=problem.seat_democrat))
        dems -= 1
        total -= 1
    elif toss == 0 and repubs != 0:
        riders.append(Thread(target=problem.seat_republican))
        repubs -= 1
        total -= 1

for rider in riders:
    rider.start()

for rider in riders:
    rider.join()