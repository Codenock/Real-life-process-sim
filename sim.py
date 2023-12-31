import random
import simpy
import numpy as np

NUM_EMPLOYEES = 2
AVG_EUPPORT_TIME = 5
CUMSTOMER_INTERVAL = 2
SIM_TIME = 120

customers_handled = 0


class CallCenter:

    def __init__(self, env, NUM_EMPLOYEES, support_time):
        self.env = env
        self.staff = simpy.Resource(env, NUM_EMPLOYEES)
        self.support_time = support_time 

    def support(self, customer):
        random_time = max(1, np.random.normal(self.support_time, 4))

        yield self.env.timeout(random_time)
        print(f"Support finished for {customer} at {self.env.now}")

def customer(env, name, call_center):
    global customers_handled
    print(f"Customer {name} enters waiting queue at {env.now:.2f}")
    with call_center.staff.request() as request:
        yield request
        print(f"Customer {name} enters call at {env.now:.2f}")
        yield env.process(call_center.support(name))
        print(f"Customer {name} left call at {env.now:.2f}")
        customers_handled += 1

def setup(env, NUM_EMPLOYEES, support_time, customer_interval):
    call_center = CallCenter(env, NUM_EMPLOYEES, support_time)

    for i in range (1, 6):
        env.process(customer(env, i, call_center))

    while True:
        yield env.timeout(random.randint(customer_interval - 1, customer_interval + 1))
        i += 1
        env.process(customer(env, NUM_EMPLOYEES, call_center))

print("Starting Call Center Simulation")
env = simpy.Environment()
env.process(setup(env, NUM_EMPLOYEES, AVG_EUPPORT_TIME, CUMSTOMER_INTERVAL))
env.run(until=SIM_TIME)

print("Customer handled " + str(customers_handled))



#Video:

#https://www.youtube.com/watch?v=8SLk_uRRcgc