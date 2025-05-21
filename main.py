# main.py
from src.simulator import test_physical_layer, test_data_link_layer, test_network_layer, test_dynamic_routing
from src.extended import test_extended_network

def run_network_simulator():
    print("\n========== ITL355: Computer Networks Lab - Network Simulator ==========\n")
    
    print("\n--- [Layer 1] PHYSICAL LAYER TEST ---")
    test_physical_layer()
    
    print("\n--- [Layer 2] DATA LINK LAYER TEST ---")
    test_data_link_layer()
    
    print("\n--- [Layer 2 Extended] EXTENDED NETWORK WITH HUBS + SWITCH ---")
    test_extended_network()

    print("\n--- [Layer 3] NETWORK LAYER - STATIC ROUTING ---")
    test_network_layer()

    print("\n--- [Layer 3] NETWORK LAYER - RIP DYNAMIC ROUTING ---")
    test_dynamic_routing()

    print("\n========== SIMULATION COMPLETED SUCCESSFULLY ==========\n")

if __name__ == "__main__":
    run_network_simulator()
