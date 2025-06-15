# main.py

from src.simulator import (
    test_physical_layer,
    test_data_link_layer,
    test_network_layer,
    test_ospf_routing,
    test_advanced_scenarios
)

from src.transport_layer import PortManager, sliding_window_transport
from src.application_layer import ChatApp, FTPMock


def test_extended_network():
    """Placeholder for extended network test"""
    print("Extended network test - implementing basic hub and switch combination")
    # You can replace this with real logic from extended.py if needed
    pass


def test_transport_and_application_layer():
    print("\n--- [Layer 4] TRANSPORT & APPLICATION LAYER TEST ---")

    # Initialize port manager for assigning ports to processes
    port_manager = PortManager()

    # ---------------- Chat Application Test ---------------- #
    print("\n[Application Test 1] ChatApp: Simulating reliable message transfer")

    chat_client = ChatApp("ChatClient")        # Sender
    chat_server = ChatApp("ChatServer")        # Receiver

    sliding_window_transport(
        sender_app=chat_client,
        receiver_app=chat_server,
        message="HelloChat",                   # Message to send
        port_manager=port_manager,
        window_size=3                          # Go-Back-N window size
    )

    # ---------------- FTP Application Test ---------------- #
    print("\n[Application Test 2] FTPMock: Simulating file upload stream")

    ftp_client = FTPMock("FTPClient")          # Sender
    ftp_server = FTPMock("FTPServer")          # Receiver

    sliding_window_transport(
        sender_app=ftp_client,
        receiver_app=ftp_server,
        message="uploadedfile",                # Simulated file data
        port_manager=port_manager,
        window_size=4                          # Larger window for FTP
    )


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

    print("\n--- [Layer 3] NETWORK LAYER - OSPF DYNAMIC ROUTING ---")
    test_ospf_routing()

    print("\n--- [Layer 3] ADVANCED NETWORK SCENARIOS ---")
    test_advanced_scenarios()

    print("\n--- [Layer 4] TRANSPORT & APPLICATION LAYER TEST ---")
    test_transport_and_application_layer()

    print("\n========== SIMULATION COMPLETED SUCCESSFULLY ==========\n")


if __name__ == "__main__":
    run_network_simulator()
