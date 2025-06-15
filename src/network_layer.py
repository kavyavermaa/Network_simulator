# src/network_layer.py
import ipaddress
import time
import random
import heapq
from collections import defaultdict

class ARP:
    """Address Resolution Protocol implementation"""
    def __init__(self):
        self.cache = {}  # IP to MAC mapping
    
    def request(self, ip_address, network):
        """Send an ARP request to find MAC address for a given IP"""
        if ip_address in self.cache:
            print(f"ARP cache hit for {ip_address} -> {self.cache[ip_address]}")
            return self.cache[ip_address]
        
        print(f"ARP request broadcast for {ip_address}")
        # sab network ko  broadcast krega
        for device in network.get_all_devices():

            #check karta hai ki device ke paas IP hai ya nahi.-hasattr(device, 'ip_address')
            if hasattr(device, 'ip_address') and device.ip_address == ip_address:
                self.cache[ip_address] = device.mac_address
                print(f"ARP reply: {ip_address} is at {device.mac_address}")
                return device.mac_address
        
        print(f"No ARP reply received for {ip_address}")
        return None

# ipv4:Network layer (Layer 3) ka ek packet hota hai jo source se destination IP address tak data bhejta hai.
class IPPacket:
    """IPv4 Packet representation"""
    def __init__(self, src_ip, dest_ip, data, ttl=64):
        self.src_ip = src_ip
        self.dest_ip = dest_ip
        self.data = data
        self.ttl = ttl  # Time To Live
        #ye dec hota hai jab rtr se pass hoa oor 0 too drop
        #infnt loop se bachne ke liye use krte hai
    
    def __str__(self):
        return f"IP Packet: {self.src_ip} -> {self.dest_ip}, TTL: {self.ttl}, Data: {self.data}"

class RoutingTableEntry:
    """Entry in a routing table"""
    def __init__(self, network, netmask, next_hop, interface, metric=1, timestamp=None):
        self.network = network  # Destination network
        self.netmask = netmask  # Subnet mask(255.255.255.0)
        self.next_hop = next_hop  # Next hop IP
        self.interface = interface  # Outgoing interface(kaunsa nic use krna hai)
        self.metric = metric  # Route cost/metric
        self.timestamp = timestamp or time.time()  # kab entry add/update hui,Zaroori hota hai dynamic routing protocols ke liye, jisme old routes expire ho jaate hain.
    
    def __str__(self):
        return f"{self.network}/{self.netmask.count('1')} via {self.next_hop} dev {self.interface} metric {self.metric}"

class Router:
    """Network layer router implementation"""
    def __init__(self, name):
        self.name = name
        self.interfaces = {}  # interface ka naam aur uske saath IP aur MAC address rakhe hote
        self.routing_table = []  # List of RoutingTableEntry objects
        self.arp = ARP()  # ARP table
        self.connected_devices = {}  # Interface to device mapping
        self.ospf = None  # OSPF instance will be initialized separately
    
    def add_interface(self, name, ip_address, mac_address, network=None):
        """Add an interface to the router"""
        # Parse IP with subnet mask (CIDR notation)
        #ipaddress module use karke subnet aur network details nikaal rahe hain.
        ip_obj = ipaddress.IPv4Interface(ip_address)
        network_addr = str(ip_obj.network.network_address)
        netmask = str(ip_obj.network.netmask)
        
        self.interfaces[name] = (str(ip_obj.ip), mac_address)
        print(f"Added interface {name} with IP {ip_address} and MAC {mac_address}")
        
        # Add a route for directly connected network
        self.add_route(network_addr, netmask, None, name, metric=0)
    
    #Ye function ek static route routing table me daalta hai.
    def add_route(self, network, netmask, next_hop, interface, metric=1):
        """Add a static route to the routing table"""
        entry = RoutingTableEntry(network, netmask, next_hop, interface, metric)
        self.routing_table.append(entry)
        print(f"Added route: {entry}")
    
    #Router interface pe koi device connect karta hai
    def connect_device(self, interface_name, device):
        """Connect a device to a router interface"""
        #agar interface valid hai toh device connect karte hain.
        if interface_name in self.interfaces:
            self.connected_devices[interface_name] = device
            print(f"Connected {device.name} to interface {interface_name}")
        else:
            print(f"Interface {interface_name} does not exist")
    
    def get_best_route(self, dest_ip):
        """Find the best route for a destination IP using longest prefix match"""
        best_match = None
        best_prefix_len = -1
        # String format wali IP address ko ek IPv4Address object mein convert kiya gaya
        dest_ip_obj = ipaddress.IPv4Address(dest_ip)
        
        for entry in self.routing_table:
            network = ipaddress.IPv4Network(f"{entry.network}/{entry.netmask}", strict=False)
            prefix_len = network.prefixlen
            
            if dest_ip_obj in network and prefix_len > best_prefix_len:
                best_match = entry
                best_prefix_len = prefix_len
        
        return best_match
    
    def forward_packet(self, packet):
        """Forward an IP packet to the next hop"""
        if packet.ttl <= 0:
            print(f"Packet dropped: TTL expired")
            return
        
        packet.ttl -= 1
        print(f"Router {self.name} forwarding packet: {packet}")
        
        # Find the best route
        route = self.get_best_route(packet.dest_ip)
        if not route:
            print(f"No route to {packet.dest_ip}")
            return
        
        # If this is the final router (destination is on a connected network)
        if route.metric == 0:  # Directly connected network
            target_ip = packet.dest_ip
            interface = route.interface
            # Use ARP to find the MAC address
            for device in self.connected_devices.values():
                if hasattr(device, 'ip_address') and device.ip_address == target_ip:
                    print(f"Delivering packet directly to {device.name}")
                    device.receive_packet(packet)
                    return
            
            print(f"Host {packet.dest_ip} not found on connected network")
            return
        
        # Forward to next hop
        next_hop = route.next_hop
        interface = route.interface
        
        if next_hop in self.connected_devices:
            next_device = self.connected_devices[next_hop]
            if hasattr(next_device, 'forward_packet'):
                next_device.forward_packet(packet)
            else:
                print(f"Next hop {next_hop} cannot forward packets")
        else:
            print(f"Next hop {next_hop} not directly connected")
    
    def print_routing_table(self):
        """Display the routing table"""
        print(f"\nRouting table for {self.name}:")
        print("Destination\t\tNetmask\t\t\tNext Hop\t\tInterface\tMetric")
        print("-" * 80)
        for entry in self.routing_table:
            print(f"{entry.network}\t\t{entry.netmask}\t\t{entry.next_hop or 'Direct'}\t\t{entry.interface}\t\t{entry.metric}")
        print()

class OSPF:
    """Open Shortest Path First protocol implementation"""
    def __init__(self, router, area=0):
        self.router = router
        self.area = area
        self.router_id = hash(router.name) % 10000000  # Simple router ID generation
        self.neighbors = {}  # Router ID to neighbor mapping
        self.lsdb = {}  # Link State Database
        self.spf_tree = {}  # Shortest Path Tree
        self.router.ospf = self  # Set reference in router
    
    def start(self, network):
        """Start the OSPF protocol"""
        print(f"Starting OSPF on router {self.router.name} (ID: {self.router_id})")
        self.network = network
        self.discover_neighbors()
        self.flood_lsa()
        self.calculate_routes()
    
    def discover_neighbors(self):
        """Discover neighboring OSPF routers"""
        print(f"Router {self.router.name} discovering OSPF neighbors")
        
        # Get all connected routers
        for interface, device in self.router.connected_devices.items():
            if isinstance(device, Router) and hasattr(device, 'ospf'):
                router_id = device.ospf.router_id
                self.neighbors[router_id] = {
                    'router': device,
                    'interface': interface,
                    'cost': 1  # Default cost
                }
                print(f"Discovered OSPF neighbor {device.name} (ID: {router_id})")
    
    def flood_lsa(self):
        """Generate and flood Link State Advertisement"""
        print(f"Router {self.router.name} flooding LSA")
        
        # Create LSA for this router
        lsa = {
            'router_id': self.router_id,
            'sequence': int(time.time()),  # Simple sequence number
            'links': {}
        }
        
        # Add links to directly connected networks
        for interface, (ip, _) in self.router.interfaces.items():
            ip_obj = ipaddress.IPv4Interface(ip)
            network_addr = str(ip_obj.network.network_address)
            prefix_len = ip_obj.network.prefixlen
            network_cidr = f"{network_addr}/{prefix_len}"
            
            lsa['links'][network_cidr] = {
                'cost': 1,
                'type': 'network'
            }
        
        # Add links to neighboring routers
        for router_id, neighbor in self.neighbors.items():
            lsa['links'][str(router_id)] = {
                'cost': neighbor['cost'],
                'type': 'router'
            }
        
        # Add to own LSDB
        self.lsdb[self.router_id] = lsa
        
        # Flood to all neighbors
        for neighbor in self.neighbors.values():
            if hasattr(neighbor['router'], 'ospf'):
                neighbor['router'].ospf.receive_lsa(lsa, self.router_id)
    
    def receive_lsa(self, lsa, from_router_id):
        """Process received LSA"""
        router_id = lsa['router_id']
        sequence = lsa['sequence']
        
        # Check if this is a new or updated LSA
        if router_id not in self.lsdb or self.lsdb[router_id]['sequence'] < sequence:
            print(f"Router {self.router.name} received new LSA from {router_id}")
            self.lsdb[router_id] = lsa
            
            # Flood to other neighbors
            for neighbor_id, neighbor in self.neighbors.items():
                if neighbor_id != from_router_id:
                    if hasattr(neighbor['router'], 'ospf'):
                        neighbor['router'].ospf.receive_lsa(lsa, self.router_id)
            
            # Recalculate routes
            self.calculate_routes()
    
    def calculate_routes(self):
        """Calculate shortest paths using Dijkstra's algorithm"""
        print(f"Router {self.router.name} calculating OSPF routes")
        
        # Clear existing OSPF routes (keep directly connected routes)
        self.router.routing_table = [route for route in self.router.routing_table if route.metric == 0]
        
        # Build graph for Dijkstra's algorithm
        graph = defaultdict(dict)
        networks = {}  # Store network information
        
        # Add links from all LSAs
        for router_id, lsa in self.lsdb.items():
            for link_id, link_data in lsa['links'].items():
                if link_data['type'] == 'router':
                    # Router-to-router link
                    try:
                        target_router_id = int(link_id)
                        graph[router_id][target_router_id] = link_data['cost']
                        graph[target_router_id][router_id] = link_data['cost']  # Bidirectional
                    except ValueError:
                        # Skip if link_id is not a valid router ID
                        continue
                elif link_data['type'] == 'network':
                    # Store network information for route calculation
                    if '/' in link_id:
                        network_addr, prefix_len = link_id.split('/')
                        networks[link_id] = {
                            'network': network_addr,
                            'prefix_len': int(prefix_len),
                            'routers': []
                        }
                        if router_id not in networks[link_id]['routers']:
                            networks[link_id]['routers'].append(router_id)
        
        # Connect routers on the same network
        for network_id, network_info in networks.items():
            routers_on_network = network_info['routers']
            for i, router1 in enumerate(routers_on_network):
                for j, router2 in enumerate(routers_on_network):
                    if i != j:
                        # Add edge between routers on same network with cost 1
                        graph[router1][router2] = 1
        
        # Dijkstra's algorithm
        distances = {self.router_id: 0}
        previous = {} #RASTA ka hisab rakhne ke liye
        nodes = list(graph.keys())
        
        while nodes:
            current = min(nodes, key=lambda node: distances.get(node, float('inf')))
            if distances.get(current, float('inf')) == float('inf'):
                break
            
            nodes.remove(current)
            
            for neighbor, cost in graph[current].items():
                if neighbor in nodes:
                    alt = distances[current] + cost
                    if alt < distances.get(neighbor, float('inf')):
                        distances[neighbor] = alt
                        previous[neighbor] = current
        
        # Add routes from SPF calculation
        for target_router_id, distance in distances.items():
            if target_router_id == self.router_id:
                continue  # Skip self
            
            # Get path to this router
            path = []
            current = target_router_id
            while current in previous:
                path.insert(0, current)
                current = previous[current]
            
            if path and target_router_id in self.lsdb:
                next_hop_id = path[0]
                
                # Find the interface to this next hop
                next_hop_router = None
                interface = None
                for neighbor_id, neighbor in self.neighbors.items():
                    if neighbor_id == next_hop_id:
                        next_hop_router = neighbor['router']
                        interface = neighbor['interface']
                        break
                
                if next_hop_router and interface:
                    # Add routes for networks advertised by this router
                    for link_id, link_data in self.lsdb[target_router_id]['links'].items():
                        if link_data['type'] == 'network' and '/' in link_id:
                            try:
                                network_addr, prefix_len = link_id.split('/')
                                netmask = self.prefix_to_netmask(int(prefix_len))
                                
                                # Check if this route already exists (avoid duplicates)
                                route_exists = False
                                for existing_route in self.router.routing_table:
                                    if (existing_route.network == network_addr and 
                                        existing_route.netmask == netmask):
                                        route_exists = True
                                        break
                                
                                if not route_exists:
                                    self.router.add_route(network_addr, netmask, 
                                                        next_hop_router.name, interface, distance)
                            except (ValueError, IndexError):
                                # Skip invalid network entries
                                continue
    
    def prefix_to_netmask(self, prefix_len):
        """Convert prefix length to netmask string"""
        return str(ipaddress.IPv4Network(f"0.0.0.0/{prefix_len}").netmask)

class NetworkDevice:
    """Network layer device with IP and MAC addresses"""
    def __init__(self, name, mac_address, ip_address=None, default_gateway=None):
        self.name = name
        self.mac_address = mac_address
        self.ip_address = ip_address
        self.default_gateway = default_gateway
        self.arp_cache = {}  # IP to MAC mapping
    
    def set_ip(self, ip_address, default_gateway=None):
        """Set the IP address and default gateway"""
        self.ip_address = ip_address
        if default_gateway:
            self.default_gateway = default_gateway
        print(f"{self.name} configured with IP {ip_address} and gateway {default_gateway}")
    
    def send_packet(self, dest_ip, data, network):
        """Create and send an IP packet"""
        packet = IPPacket(self.ip_address, dest_ip, data)
        print(f"{self.name} sending packet to {dest_ip}: {data}")
        
        # Check if destination is on same network
        src_net = ipaddress.IPv4Interface(self.ip_address).network
        dest_net = ipaddress.IPv4Network(f"{dest_ip}/{src_net.prefixlen}", strict=False)
        
        if dest_net == src_net:
            # Destination is on the same network
            # Use ARP to find MAC address
            for device in network.get_all_devices():
                if hasattr(device, 'ip_address') and device.ip_address == dest_ip:
                    print(f"Delivering packet directly to {device.name}")
                    device.receive_packet(packet)
                    return
            
            print(f"Host {dest_ip} not found on local network")
        else:
            # Send to default gateway
            if not self.default_gateway:
                print(f"No default gateway configured")
                return
            
            # Find the gateway device
            for device in network.get_all_devices():
                #Gateway ka IP find karo aur forward_packet call karo.
                if hasattr(device, 'ip_address') and device.ip_address == self.default_gateway:
                    if hasattr(device, 'forward_packet'):
                        print(f"Sending packet to gateway {self.default_gateway}")
                        device.forward_packet(packet)
                        return
                    else:
                        print(f"Gateway {self.default_gateway} cannot forward packets")
                        return
            
            print(f"Gateway {self.default_gateway} not found")
    
    def receive_packet(self, packet):
        """Process a received IP packet"""
        if packet.dest_ip == self.ip_address:
            print(f"{self.name} received packet: {packet}")
            # Process the packet data
            return True
        else:
            print(f"{self.name} discarding packet not addressed to me")
            return False