import random
import time

class Switch:
    def __init__(self, name):
        self.name = name
        self.mac_table = {}

    def connect(self, device, mac_address):
        self.mac_table[mac_address] = device
        print(f"{device.name} with MAC {mac_address} connected to {self.name}")

    def forward_frame(self, source_mac, dest_mac, data):
        if source_mac not in self.mac_table:
            print(f"Learning MAC address {source_mac}")
            self.mac_table[source_mac] = self.mac_table.get(source_mac)

        if dest_mac in self.mac_table and self.mac_table[dest_mac] is not None:
            print(f"Switch forwarding data from {source_mac} to {dest_mac}")
            self.mac_table[dest_mac].receive_data(data)
        else:
            print(f"Broadcasting data since {dest_mac} is unknown")
            for device in self.mac_table.values():
                if device is not None and device.mac_address != source_mac:
                    device.receive_data(data)

class Device:
    def __init__(self, name, mac_address):
        self.name = name
        self.mac_address = mac_address

    def send_data(self, switch, dest_mac, data):
        print(f"{self.name} sending data to {dest_mac}")
        switch.forward_frame(self.mac_address, dest_mac, data)

    def receive_data(self, data):
        print(f"{self.name} received: {data}")

def parity_check(data):
    ones_count = data.count('1')
    return ones_count % 2 == 0

def csma_cd(transmitting_device, switch, dest_mac, data, max_retries=5):
    retries = 0
    while retries < max_retries:
        if random.random() < 0.2: 
            print("Collision detected! Initiating jamming and backoff...")

            # Jamming: Inform other devices that a collision has occurred
            print("Jamming the network...")
            transmitting_device.send_data(switch, transmitting_device.mac_address, "JAM_SIGNAL")

            # Backoff: Wait for a random backoff time (exponential backoff)
            backoff_time = random.uniform(0, 2 ** retries)
            print(f"Backing off for {backoff_time:.2f} seconds...")
            time.sleep(backoff_time)  # Simulate backoff time

            retries += 1  # Increment retry count
            print(f"Retrying transmission ({retries}/{max_retries})...")
        else:
            transmitting_device.send_data(switch, dest_mac, data)
            return  # Transmission successful, exit loop

    print(f"Max retries reached ({max_retries}). Transmission failed.")

def sliding_window(devices, switch, dest_mac, data, window_size=3):
    print(f"Initiating Sliding Window Protocol with window size: {window_size}")
    total_frames = len(data)
    sent = 0

    while sent < total_frames:
        window_end = min(sent + window_size, total_frames)
        print(f"Sending frames {sent + 1} to {window_end}")

        for i in range(sent, window_end):
            print(f"Frame {i + 1} sent: {data[i]}")
            devices[0].send_data(switch, dest_mac, data[i])

        ack_received = random.choice([True, False])
        if ack_received:
            print("Acknowledgment received.")
            sent = window_end  # Slide window forward
        else:
            print("No acknowledgment received. Resending frames...")

        for i in range(sent, window_end):
             print(f"Retransmitting Frame {i + 1}: {data[i]}")
             devices[0].send_data(switch, dest_mac,data[i])
                                  
    print("Sliding Window Protocol completed.")