"""
Simulating Container Terminal Process with simpy
"""
import simpy 
import random

class ContainerTerminal:

    def __init__(self, env):
        self.env = env
        self.berth = simpy.Resource(env, capacity=2)
        self.quay_crane = simpy.Resource(env, capacity=2)
        self.truck = simpy.Resource(env, capacity=3)

    def berth_vessel(self, vessel_id):

        """
        This method is to allocate berth to the vessels already present at the container terminal
        """
        print(f"Time:{self.env.now:.0f} | Action: Vessel_{vessel_id} is berthing")
        yield self.env.timeout(10)  # delay added for  berthing

    def unload_container(self, vessel_id, container_id):
        """
        This method is to  allocate quay crane to the vessels present in the berth to proceed with container unloading
        """
        print(f"Time:{self.env.now:.0f} | Action:Crane is unloading container {container_id} from vessel_{vessel_id}")
        yield self.env.timeout(3)  # delay added to unload a container

    def move_container_to_yard(self, vessel_id, container_id):

        """
        This method is to allocate truck to drop off the container at the yard block
        """
        print(f"Time:{self.env.now:.0f} | Action :Truck is moving container {container_id} from vessel_{vessel_id} to the yard")
        yield self.env.timeout(6)  # delay added for truck to drop off the container at the yard block and come back again


class Vessel:

    def __init__(self,env,terminal):
        self.env=env
        self.terminal=terminal

    def process(self,vessel_id):
        """
         This method simulates the entire process of 
         vessel arrival--->vessel berthing--->container unloading --> transporting containers to yard block
        """
        print(f"Time:{self.env.now:.0f} | Action: vessel_{vessel_id} has arrived at container terminal")
        
        #Process:Berthing
        with self.terminal.berth.request() as berth_request:
            yield berth_request #wait for an available berth
            yield self.env.process(self.terminal.berth_vessel(vessel_id)) #if berth is available start the berthing process
 
            #Process:Unload container
            with self.terminal.quay_crane.request() as quay_crane_request:
                yield quay_crane_request #wait for an available quay crane

                #if quay crane is available start the container unloading process
                for container_id in range(1,51):
                    yield self.env.process(self.terminal.unload_container(vessel_id,container_id))

                    #Process: Ship container to yard
                    with self.terminal.truck.request() as truck_request:
                            yield truck_request  # Wait for a free truck
                            #if free truck is available start shipping container to yard
                            yield self.env.process(self.terminal.move_container_to_yard(vessel_id, container_id))  # Move container to yard
        
        print(f"Time:{self.env.now:.0f} | Action :vessel_{vessel_id} has completed unloading")

    def arrival(self):
        """
        This method  simulates the arrival of vessel at the container terminal .The time between vessel arrivals follows an
        exponential distribution with an average of 5 hours.
        """
        id=1
        while True:
            yield self.env.timeout(random.expovariate(1/10)) # add a delay to vessel arrival time
            self.env.process(self.process(id)) # starts the container terminal simulation for the current vessel
            id+=1

if __name__=="__main__":
    # Run the simulation
    print("========================== CONTAINER TERMINAL SIMULATION =========================")
    print("----------------------------------------------------------------------------------")
    env=simpy.Environment()
    print("                             Environment Created                                  ")
    container_terminal=ContainerTerminal(env)
    print("----------------------------------------------------------------------------------")
    vessel=Vessel(env,container_terminal)
    print("                              Starting Simulation                                 ")
    print("----------------------------------------------------------------------------------")
    print('Time | Action')
    print("----------------------------------------------------------------------------------")
    env.process(vessel.arrival())
  
    env.run(until=24*60)
