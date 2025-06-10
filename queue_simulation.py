import simpy
import random

# Set random seed for reproducibility
# testing code lines
random.seed(42)

# Parameters
INTER_ARRIVAL_TIME = 15  # average time between customer arrivals
SERVICE_TIME = 6         # average service time per customer
SIMULATION_TIME = 5000   # total simulation time

def customer(env, server, wait_times):
    arrival_time = env.now
    with server.request() as request:
        yield request
        wait = env.now - arrival_time
        wait_times.append(wait)
        service_duration = random.expovariate(1.0 / SERVICE_TIME)
        yield env.timeout(service_duration)

def source(env, server, wait_times):
    while True:
        yield env.timeout(random.expovariate(1.0 / INTER_ARRIVAL_TIME))
        env.process(customer(env, server, wait_times))

def run_simulation():
    env = simpy.Environment()
    server = simpy.Resource(env, capacity=1)
    wait_times = []

    env.process(source(env, server, wait_times))
    env.run(until=SIMULATION_TIME)

    avg_wait = sum(wait_times) / len(wait_times) if wait_times else 0
    max_wait = max(wait_times) if wait_times else 0

    print(f"Average wait time: {avg_wait:.2f}")
    print(f"Max wait time: {max_wait:.2f}")

if __name__ == "__main__":
    run_simulation()
