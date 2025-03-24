Network Simulator - Project Overview
This project is a network simulator that simulates various network layers, including the Physical Layer and Data Link Layer, and visualizes the network topology in a Cisco-style layout. The project demonstrates the core concepts of network communication, protocols, and network visualization.

Table of Contents
Project Objective

How the Project Was Started

Project Structure

Key Features & Functionality

Testing & Simulation

Network Visualization

How to Run the Project and see simulations

Conclusion

Project Objective
The goal of this project is to develop a network simulator that mimics the physical and data link layers of computer networking. The simulator:

Simulates basic network operations between devices.

Implements fundamental data link protocols like CSMA/CD (Carrier Sense Multiple Access with Collision Detection) and Sliding Window Protocol for flow control.

Simulates network communication through EndDevices, Hubs, and Switches.

Visualizes network topologies in a Cisco-style layout using networkx and matplotlib.

How the Project Was Started
This project began with an understanding of basic computer network principles, including the OSI (Open Systems Interconnection) model. The objective was to create a network simulator to simulate real-world protocols used for device communication at the Physical Layer (Layer 1) and Data Link Layer (Layer 2).

Key Steps Involved:
Conceptualizing the Network Layers:

Started by simulating the Physical Layer with EndDevices and Hubs to establish basic connectivity.

Implemented the Data Link Layer with Switches and protocols like CSMA/CD and Sliding Window to handle data transmission, error control, and flow control.

Visualization:

A major focus was on representing the network in a way that resembles real-world network topologies (like those in Cisco systems).

networkx and matplotlib were used for plotting network topologies and for providing a graphical representation of devices and their connections.

Testing and Debugging:

Tests were written for both the Physical Layer and Data Link Layer to simulate how devices communicate through Hub and Switch using real-world protocols.

The final testing simulated a more extended network with two star topologies connected through a Switch to verify the scalability and interaction of the devices.

Project Structure
The project is organized into the following core files:

simulator.py:

This file contains the core logic for simulating the Physical Layer and Data Link Layer, including the implementation of various network devices (EndDevice, Hub, Switch), protocols (CSMA/CD, Sliding Window), and visualization.

tests/:

Contains separate test files for testing different parts of the simulation:

test_data_link_layer.py: Tests the functionality of the Switch and the Data Link Layer protocols.

test_physical_layer.py: Simulates basic communication between devices through a Hub at the Physical Layer.

main.py:

The entry point that runs the tests and demonstrates the simulation of the Physical Layer, Data Link Layer, and an Extended Network with two star topologies.

src/:

Contains all the classes (EndDevice, Hub, Switch, Device) and functions that simulate the network layers and protocols.

Key Features & Functionality
Physical Layer Simulation:

EndDevices and Hubs are used to simulate simple network communication.

Devices communicate via broadcasting in case of a Hub. Data can be sent between devices using Connections.

Data Link Layer Simulation:

Switches are implemented to simulate MAC address-based communication.

Parity Check: Ensures data integrity by checking for data corruption.

CSMA/CD (Carrier Sense Multiple Access with Collision Detection): Simulates how devices avoid data collision in shared networks.

Sliding Window Protocol: Manages data flow between sender and receiver by sending data in smaller frames.

Extended Network Simulation:

Two star topologies with Hubs are connected to a Switch, and communication is facilitated across the entire network.

This test simulates a larger network involving multiple devices and hubs connected through a central switch.

Visualization:

Network topologies are visualized in a Cisco-style layout using networkx for graph creation and matplotlib for visualization.

Devices are color-coded and shaped differently for easy identification (blue circles for EndDevices, red squares for Switches, and green pentagons for Hubs).

Testing & Simulation
Test 1: test_physical_layer()
Objective: Tests the basic functionality of the Physical Layer.

What It Does:

Two EndDevices (device1 and device2) are connected through a Connection object.

A Hub connects multiple devices, and device1 sends data to all other connected devices.

Verifies the broadcasting functionality of a Hub.

Test 2: test_data_link_layer()
Objective: Tests the Data Link Layer protocols and Switch functionality.

What It Does:

Creates a Switch and connects five devices.

Simulates Parity Check, CSMA/CD, and Sliding Window Protocol to ensure proper error handling and flow control.

Verifies data transmission between devices using these protocols.

Test 3: test_extended_network()
Objective: Tests a more complex network with multiple devices and hubs connected through a Switch.

What It Does:

Two star topologies with Hubs are connected to a Switch.

Devices in both hubs communicate using CSMA/CD.

Verifies the scalability of the network and the performance of the Switch in routing data.

Network Visualization
To provide a clearer understanding of the network setup and make it look professional, the network is visualized in a Cisco-style layout. The visualization is done using networkx and matplotlib to generate and display the network diagram.

Key Visualization Features:
Devices are represented with distinct shapes (circle for EndDevices, square for Switch, pentagon for Hub).

Nodes are colored based on their type (blue for EndDevices, red for Switches, green for Hubs).

Network gridlines and a title are added to give the network a structured, professional look.

How to Run the Project
Requirements:
Python 3.x

Install required libraries:

networkx: For network graph creation.

matplotlib: For plotting network diagrams.

To install dependencies, use:

bash
Copy
pip install networkx matplotlib
Running the Project:
Clone the repository or download the files.

Open a terminal/command prompt and navigate to the project directory.

Run the main.py file to execute the tests and see the simulation:

bash
Copy
python main.py
This will run all three tests (Physical Layer, Data Link Layer, Extended Network) and display the network visualizations