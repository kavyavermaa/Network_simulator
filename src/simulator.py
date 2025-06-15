# src/simulator.py
import networkx as nx
import matplotlib.pyplot as plt
import random
import ipaddress
from src.physical_layer import EndDevice, Hub, Connection
from src.data_link_layer import Switch, Device, parity_check, csma_cd, sliding_window
from src.network_layer import Router, NetworkDevice, IPPacket, ARP, OSPF

class Network:
    """Network class to manage all devices"""
    def __init__(self):
        self.devices = []
    
    def add_device(self, device):
        self.devices.append(device)
    
    def get_all_devices(self):
        return self.devices

def visualize_network(devices, connections, title="Network Topology"):
    G = nx.Graph()

    for device in devices:
        if isinstance(device, Router):
            color = "red"
            label = f"{device.name}"
            if hasattr(device, 'interfaces'):
                ips = [ip for ip, _ in device.interfaces.values()]
                if ips:
                    label += f"\n{ips[0]}"
        elif isinstance(device, NetworkDevice):
            color = "blue"
            label = f"{device.name}\n{device.ip_address}"
        elif isinstance(device, EndDevice):
            color = "blue"
            label = device.name
        elif isinstance(device, Switch):
            color = "green"
            label = device.name
        else:
            color = "gray"
            label = device.name
        
        G.add_node(device.name, color=color, label=label)

    for conn in connections:
        G.add_edge(conn[0].name, conn[1].name)

    colors = [G.nodes[n].get("color", "gray") for n in G.nodes]
    labels = {n: G.nodes[n].get("label", n) for n in G.nodes}

    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G, seed=42)  # For consistent layout
    nx.draw(G, pos, with_labels=False, node_color=colors, node_size=2000, edge_color="gray")
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=8)
    plt.title(title)
    plt.show(block=False)
    plt.pause(5)
    plt.close()

def test_physical_layer():
    print("\n--- Testing Physical Layer ---")
    network = Network()
    
    device1 = EndDevice("Device1")
    device2 = EndDevice("Device2")
    network.add_device(device1)
    network.add_device(device2)
    
    connection = Connection(device1, device2)

    device1.send_data("Hello, Device2!", connection)

    hub = Hub("Hub1")
    device3 = EndDevice("Device3")
    device4 = EndDevice("Device4")
    device5 = EndDevice("Device5")
    device6 = EndDevice("Device6")
    
    network.add_device(hub)
    network.add_device(device3)
    network.add_device(device4)
    network.add_device(device5)
    network.add_device(device6)

    hub.connect(device1)
    hub.connect(device2)
    hub.connect(device3)
    hub.connect(device4)
    hub.connect(device5)
    hub.connect(device6)

    device1.send_data("Hello, everyone!", hub)

    devices = [device1, device2, device3, device4, device5, device6, hub]
    connections = [(device1, hub), (device2, hub), (device3, hub), (device4, hub), (device5, hub), (device6, hub)]
    visualize_network(devices, connections, "Physical Layer: Hub Topology")

def test_data_link_layer():
    print("\n--- Testing Data Link Layer ---")
    network = Network()
    
    try:
        switch = Switch("Switch1")
        network.add_device(switch)
        devices = [Device(f"D{i+1}", f"AA:BB:CC:DD:EE:0{i+1}") for i in range(5)]
        
        for device in devices:
            network.add_device(device)
            switch.connect(device, device.mac_address)

        data = "1010101"  # Example data for parity check
        print("Running Parity Check...")
        if parity_check(data):
            print("Parity Check Passed, attempting CSMA/CD...")
            csma_cd(devices[0], switch, devices[1].mac_address, data)
        else:
            print("Data corrupted! Not sending.")

        print("Running Sliding Window Protocol...")
        sliding_window(devices, switch, devices[2].mac_address, "110011001100", window_size=2)

        visualize_network([switch] + devices, [(device, switch) for device in devices],
                          "Data Link Layer: Switch Topology")
        print("Data Link Layer Test Completed Successfully!")

    except Exception as e:
        print(f"Error during Data Link Layer testing: {e}")

def test_network_layer():
    print("\n--- Testing Network Layer ---")
    network = Network()
    
    # Create routers
    router1 = Router("Router1")
    router2 = Router("Router2")
    router3 = Router("Router3")
    
    network.add_device(router1)
    network.add_device(router2)
    network.add_device(router3)
    
    # Create network devices (hosts) and harr host ka nam and mac add.
    host1 = NetworkDevice("Host1", "AA:BB:CC:11:11:11")
    host2 = NetworkDevice("Host2", "AA:BB:CC:22:22:22")
    host3 = NetworkDevice("Host3", "AA:BB:CC:33:33:33")
    host4 = NetworkDevice("Host4", "AA:BB:CC:44:44:44")
    host5 = NetworkDevice("Host5", "AA:BB:CC:55:55:55")
    host6 = NetworkDevice("Host6", "AA:BB:CC:66:66:66")
    
    network.add_device(host1)
    network.add_device(host2)
    network.add_device(host3)
    network.add_device(host4)
    network.add_device(host5)
    network.add_device(host6)
    
    # Configure router interfaces
    router1.add_interface("eth0", "192.168.1.1/24", "AA:BB:CC:01:01:01")
    router1.add_interface("eth1", "10.0.0.1/24", "AA:BB:CC:01:01:02")
    
    router2.add_interface("eth0", "10.0.0.2/24", "AA:BB:CC:02:02:01")
    router2.add_interface("eth1", "192.168.2.1/24", "AA:BB:CC:02:02:02")
    
    router3.add_interface("eth0", "192.168.1.2/24", "AA:BB:CC:03:03:01")
    router3.add_interface("eth1", "192.168.3.1/24", "AA:BB:CC:03:03:02")
    
    # Configure hosts with proper IP addresses including subnet mask
    host1.set_ip("192.168.1.10/24", "192.168.1.1")
    host2.set_ip("192.168.1.11/24", "192.168.1.1")
    host3.set_ip("192.168.2.10/24", "192.168.2.1")
    host4.set_ip("192.168.2.11/24", "192.168.2.1")
    host5.set_ip("192.168.3.10/24", "192.168.3.1")
    host6.set_ip("192.168.3.11/24", "192.168.3.1")
    
    # Connect devices to routers (simulating physical connections)
    router1.connect_device("eth0", host1)
    router1.connect_device("eth0", host2)
    router1.connect_device("eth0", router3)  # Router3 is also on this network
    router1.connect_device("eth1", router2)
    
    router2.connect_device("eth0", router1)
    router2.connect_device("eth1", host3)
    router2.connect_device("eth1", host4)
    
    router3.connect_device("eth0", router1)
    router3.connect_device("eth0", host1)  
    router3.connect_device("eth0", host2) 
    router3.connect_device("eth1", host5)
    router3.connect_device("eth1", host6)
    
    # Add static routes for inter-network communication
    router1.add_route("192.168.2.0", "255.255.255.0", "Router2", "eth1")
    router1.add_route("192.168.3.0", "255.255.255.0", "Router3", "eth0")
    
    router2.add_route("192.168.1.0", "255.255.255.0", "Router1", "eth0")
    router2.add_route("192.168.3.0", "255.255.255.0", "Router1", "eth0")
    
    router3.add_route("192.168.2.0", "255.255.255.0", "Router1", "eth0")
    router3.add_route("10.0.0.0", "255.255.255.0", "Router1", "eth0")
    
    # Display routing tables
    router1.print_routing_table()
    router2.print_routing_table()
    router3.print_routing_table()
    
    # Test ARP
    print("\n--- Testing ARP Protocol ---")
    arp = ARP()
    mac = arp.request("192.168.1.10", network)
    print(f"ARP result for 192.168.1.10: {mac}")
    
    # Test packet forwarding
    print("\n--- Testing Packet Forwarding with Static Routing ---")
    # Host1 sends data to Host3 (across routers)
    host1.send_packet("192.168.2.10", "Hello from Host1 to Host3", network)
    
    # Host2 sends data to Host5 (across routers)
    host2.send_packet("192.168.3.10", "Hello from Host2 to Host5", network)
    
    # Test local network communication
    print("\n--- Testing Local Network Communication ---")
    host1.send_packet("192.168.1.11", "Hello from Host1 to Host2 (same network)", network)
    
    # Visualize network
    devices = [router1, router2, router3, host1, host2, host3, host4, host5, host6]
    connections = [
        (router1, host1), (router1, host2), (router1, router2), (router1, router3),
        (router2, host3), (router2, host4),
        (router3, host5), (router3, host6)
    ]
    visualize_network(devices, connections, "Network Layer: Static Routing")
    
    print("Network Layer Static Routing Test Completed")

def test_ospf_routing():
    print("\n--- Testing OSPF Dynamic Routing ---")
    network = Network()
    
    # Create routers
    router1 = Router("Router1")
    router2 = Router("Router2")
    router3 = Router("Router3")
    router4 = Router("Router4")
    
    network.add_device(router1)
    network.add_device(router2)
    network.add_device(router3)
    network.add_device(router4)
    
    # Create hosts
    host1 = NetworkDevice("Host1", "AA:BB:CC:11:11:11")
    host2 = NetworkDevice("Host2", "AA:BB:CC:22:22:22")
    host3 = NetworkDevice("Host3", "AA:BB:CC:33:33:33")
    host4 = NetworkDevice("Host4", "AA:BB:CC:44:44:44")
    
    network.add_device(host1)
    network.add_device(host2)
    network.add_device(host3)
    network.add_device(host4)
    
    # Configure router interfaces for OSPF topology
    router1.add_interface("eth0", "10.0.1.1/24", "AA:BB:CC:01:01:01")      # Host network
    router1.add_interface("eth1", "10.0.12.1/24", "AA:BB:CC:01:01:02")     # To Router2
    router1.add_interface("eth2", "10.0.13.1/24", "AA:BB:CC:01:01:03")     # To Router3
    
    router2.add_interface("eth0", "10.0.12.2/24", "AA:BB:CC:02:02:01")     # To Router1
    router2.add_interface("eth1", "10.0.2.1/24", "AA:BB:CC:02:02:02")      # Host network
    router2.add_interface("eth2", "10.0.24.1/24", "AA:BB:CC:02:02:03")     # To Router4
    
    router3.add_interface("eth0", "10.0.13.2/24", "AA:BB:CC:03:03:01")     # To Router1
    router3.add_interface("eth1", "10.0.3.1/24", "AA:BB:CC:03:03:02")      # Host network
    router3.add_interface("eth2", "10.0.34.1/24", "AA:BB:CC:03:03:03")     # To Router4
    
    router4.add_interface("eth0", "10.0.24.2/24", "AA:BB:CC:04:04:01")     # To Router2
    router4.add_interface("eth1", "10.0.34.2/24", "AA:BB:CC:04:04:02")     # To Router3
    router4.add_interface("eth2", "10.0.4.1/24", "AA:BB:CC:04:04:03")      # Host network
    
    # Configure hosts
    host1.set_ip("10.0.1.10/24", "10.0.1.1")
    host2.set_ip("10.0.2.10/24", "10.0.2.1")
    host3.set_ip("10.0.3.10/24", "10.0.3.1")
    host4.set_ip("10.0.4.10/24", "10.0.4.1")
    
    # Connect devices to routers
    router1.connect_device("eth0", host1)
    router1.connect_device("eth1", router2)
    router1.connect_device("eth2", router3)
    
    router2.connect_device("eth0", router1)
    router2.connect_device("eth1", host2)
    router2.connect_device("eth2", router4)
    
    router3.connect_device("eth0", router1)
    router3.connect_device("eth1", host3)
    router3.connect_device("eth2", router4)
    
    router4.connect_device("eth0", router2)
    router4.connect_device("eth1", router3)
    router4.connect_device("eth2", host4)
    
    # Initialize OSPF on all routers
    ospf1 = OSPF(router1, area=0)
    ospf2 = OSPF(router2, area=0)
    ospf3 = OSPF(router3, area=0)
    ospf4 = OSPF(router4, area=0)
    
    # Start OSPF protocol
    print("\n--- Starting OSPF Protocol ---")
    ospf1.start(network)
    ospf2.start(network)
    ospf3.start(network)
    ospf4.start(network)
    
    # Display routing tables after OSPF convergence
    print("\n--- Routing Tables After OSPF Convergence ---")
    router1.print_routing_table()
    router2.print_routing_table()
    router3.print_routing_table()
    router4.print_routing_table()
    
    # Test packet forwarding with OSPF routes
    print("\n--- Testing Packet Forwarding with OSPF ---")
    host1.send_packet("10.0.4.10", "Hello from Host1 to Host4 via OSPF routes", network)
    host2.send_packet("10.0.3.10", "Hello from Host2 to Host3 via OSPF routes", network)
    
    # Visualize OSPF network
    devices = [router1, router2, router3, router4, host1, host2, host3, host4]
    connections = [
        (router1, host1), (router1, router2), (router1, router3),
        (router2, host2), (router2, router4),
        (router3, host3), (router3, router4),
        (router4, host4)
    ]
    visualize_network(devices, connections, "Network Layer: OSPF Dynamic Routing")
    
    print("OSPF Dynamic Routing Test Completed")

def test_advanced_scenarios():
    print("\n--- Testing Advanced Network Scenarios ---")
    network = Network()
    
    # Create a more complex topology
    routers = []
    for i in range(5):
        router = Router(f"Router{i+1}")
        routers.append(router)
        network.add_device(router)
    
    hosts = []
    for i in range(6):
        host = NetworkDevice(f"Host{i+1}", f"AA:BB:CC:DD:EE:{i+1:02d}")
        hosts.append(host)
        network.add_device(host)
    
    # Configure a complex network topology
    #Ye comment hai jo batata hai ki ab hum network ki structure set karenge, matlab kaunse router kaunsa IP address use karega, aur kaunse devices connected hain.
    # Router1: Central hub
    routers[0].add_interface("eth0", "192.168.1.1/24", "AA:BB:CC:01:01:01")  # Hosts
    routers[0].add_interface("eth1", "10.0.12.1/24", "AA:BB:CC:01:01:02")    # To Router2
    routers[0].add_interface("eth2", "10.0.13.1/24", "AA:BB:CC:01:01:03")    # To Router3
    routers[0].add_interface("eth3", "10.0.14.1/24", "AA:BB:CC:01:01:04")    # To Router4
    
    # Router2: Branch office
    routers[1].add_interface("eth0", "10.0.12.2/24", "AA:BB:CC:02:02:01")    # To Router1
    routers[1].add_interface("eth1", "192.168.2.1/24", "AA:BB:CC:02:02:02")  # Hosts
    routers[1].add_interface("eth2", "10.0.25.1/24", "AA:BB:CC:02:02:03")    # To Router5
    
    # Router3: Another branch
    routers[2].add_interface("eth0", "10.0.13.2/24", "AA:BB:CC:03:03:01")    # To Router1
    routers[2].add_interface("eth1", "192.168.3.1/24", "AA:BB:CC:03:03:02")  # Hosts
    
    # Router4: Backup path
    routers[3].add_interface("eth0", "10.0.14.2/24", "AA:BB:CC:04:04:01")    # To Router1
    routers[3].add_interface("eth1", "10.0.45.1/24", "AA:BB:CC:04:04:02")    # To Router5
    
    # Router5: Remote office
    routers[4].add_interface("eth0", "10.0.25.2/24", "AA:BB:CC:05:05:01")    # To Router2
    routers[4].add_interface("eth1", "10.0.45.2/24", "AA:BB:CC:05:05:02")    # To Router4
    routers[4].add_interface("eth2", "192.168.5.1/24", "AA:BB:CC:05:05:03")  # Hosts
    
    # Configure hosts
    hosts[0].set_ip("192.168.1.10/24", "192.168.1.1")  # Connected to Router1
    hosts[1].set_ip("192.168.1.11/24", "192.168.1.1")  # Connected to Router1
    hosts[2].set_ip("192.168.2.10/24", "192.168.2.1")  # Connected to Router2
    hosts[3].set_ip("192.168.3.10/24", "192.168.3.1")  # Connected to Router3
    hosts[4].set_ip("192.168.5.10/24", "192.168.5.1")  # Connected to Router5
    hosts[5].set_ip("192.168.5.11/24", "192.168.5.1")  # Connected to Router5
    
    # Connect devices
    routers[0].connect_device("eth0", hosts[0])
    routers[0].connect_device("eth0", hosts[1])
    routers[0].connect_device("eth1", routers[1])
    routers[0].connect_device("eth2", routers[2])
    routers[0].connect_device("eth3", routers[3])
    
    routers[1].connect_device("eth0", routers[0])
    routers[1].connect_device("eth1", hosts[2])
    routers[1].connect_device("eth2", routers[4])
    
    routers[2].connect_device("eth0", routers[0])
    routers[2].connect_device("eth1", hosts[3])
    
    routers[3].connect_device("eth0", routers[0])
    routers[3].connect_device("eth1", routers[4])
    
    routers[4].connect_device("eth0", routers[1])
    routers[4].connect_device("eth1", routers[3])
    routers[4].connect_device("eth2", hosts[4])
    routers[4].connect_device("eth2", hosts[5])
    
    # Add static routes for this complex topology
    # Router1 routes
    routers[0].add_route("192.168.2.0", "255.255.255.0", "Router2", "eth1")
    routers[0].add_route("192.168.3.0", "255.255.255.0", "Router3", "eth2")
    routers[0].add_route("192.168.5.0", "255.255.255.0", "Router2", "eth1")  # Via Router2
    
    # Router2 routes
    routers[1].add_route("192.168.1.0", "255.255.255.0", "Router1", "eth0")
    routers[1].add_route("192.168.3.0", "255.255.255.0", "Router1", "eth0")
    routers[1].add_route("192.168.5.0", "255.255.255.0", "Router5", "eth2")
    
    # Router3 routes
    routers[2].add_route("192.168.1.0", "255.255.255.0", "Router1", "eth0")
    routers[2].add_route("192.168.2.0", "255.255.255.0", "Router1", "eth0")
    routers[2].add_route("192.168.5.0", "255.255.255.0", "Router1", "eth0")
    
    # Router4 routes
    routers[3].add_route("192.168.1.0", "255.255.255.0", "Router1", "eth0")
    routers[3].add_route("192.168.2.0", "255.255.255.0", "Router1", "eth0")
    routers[3].add_route("192.168.3.0", "255.255.255.0", "Router1", "eth0")
    routers[3].add_route("192.168.5.0", "255.255.255.0", "Router5", "eth1")
    
    # Router5 routes
    routers[4].add_route("192.168.1.0", "255.255.255.0", "Router2", "eth0")
    routers[4].add_route("192.168.2.0", "255.255.255.0", "Router2", "eth0")
    routers[4].add_route("192.168.3.0", "255.255.255.0", "Router2", "eth0")
    
    # Display all routing tables
    print("\n--- Complex Network Routing Tables ---")
    for router in routers:
        router.print_routing_table()
    
    # Test various communication scenarios
    print("\n--- Testing Complex Network Communication ---")
    hosts[0].send_packet("192.168.5.10", "Message from Host1 to Host5", network)
    hosts[2].send_packet("192.168.3.10", "Message from Host3 to Host4", network)
    hosts[4].send_packet("192.168.1.11", "Message from Host5 to Host2", network)
    
    # Test TTL expiration
    print("\n--- Testing TTL Expiration ---")
    packet = IPPacket("192.168.1.10", "192.168.5.10", "Test TTL", ttl=1)
    routers[0].forward_packet(packet)
    
    # Visualize complex network
    devices = routers + hosts
    connections = [
        (routers[0], hosts[0]), (routers[0], hosts[1]),
        (routers[0], routers[1]), (routers[0], routers[2]), (routers[0], routers[3]),
        (routers[1], hosts[2]), (routers[1], routers[4]),
        (routers[2], hosts[3]),
        (routers[3], routers[4]),
        (routers[4], hosts[4]), (routers[4], hosts[5])
    ]
    visualize_network(devices, connections, "Advanced Network Scenarios")
    
    print("Advanced Network Scenarios Test Completed")

def main():
    print("Network Simulator")
    print("=================")
    
    # Uncomment the tests you want to run
    # test_physical_layer()
    # test_data_link_layer()
    test_network_layer()
    test_ospf_routing()
    test_advanced_scenarios()

if __name__ == "__main__":
    main()