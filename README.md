                                  Container Terminal Simulation

This project simulates operations at a container terminal using SimPy. The simulation models vessel arrivals, berthing, unloading containers, and moving them to the yard using trucks.

Requirements
Python 3.x
SimPy (pip install simpy)


How It Works
ContainerTerminal: Manages resources (berths, cranes, trucks) and operations like berthing, unloading, and transporting containers.

Vessel: Simulates vessel arrival, berthing, container unloading, and transportation to the yard.

Process:
Vessel arrives at the terminal.
Berths are allocated.
Containers are unloaded and transported to the yard.

Run the simulation:
pip install -r requirement.txt
python simulator.py
