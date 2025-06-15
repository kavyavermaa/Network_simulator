# src/transport_layer.py

class PortManager:
    def __init__(self):
        self.well_known_ports = {
            "FTP": 21,
            "TELNET": 23,
            "HTTP": 80,
            "SSH": 22
        }
        self.ephemeral_start = 49152
        self.next_ephemeral = self.ephemeral_start
        self.process_table = {}  # Maps process name to port number

    def assign_port(self, process_name):
        if process_name in self.well_known_ports:
            return self.well_known_ports[process_name]
        if process_name not in self.process_table:
            self.process_table[process_name] = self.next_ephemeral
            self.next_ephemeral += 1
        return self.process_table[process_name]


class TCPSegment:
    def __init__(self, src_port, dest_port, seq, ack, data, flags="ACK"):
        self.src_port = src_port
        self.dest_port = dest_port
        self.seq = seq
        self.ack = ack
        self.data = data
        self.flags = flags

    def __str__(self):
        return (f"[TCP SEGMENT] SrcPort={self.src_port}, DestPort={self.dest_port}, "
                f"Seq={self.seq}, Ack={self.ack}, Flags={self.flags}, Data={self.data}")


def sliding_window_transport(sender_app, receiver_app, message, port_manager, window_size=3):
    print(f"\n[Transport Layer] Starting Go-Back-N Sliding Window (win size={window_size})")
    sender_port = port_manager.assign_port(sender_app.name)
    receiver_port = port_manager.assign_port(receiver_app.name)

    frames = [message[i:i + 1] for i in range(len(message))]  # Send 1 char per frame
    seq = 0
    ack = 0
    total = len(frames)

    while seq < total:
        window_end = min(seq + window_size, total)
        print(f"\nSending window: [{seq} - {window_end - 1}]")

        for i in range(seq, window_end):
            segment = TCPSegment(sender_port, receiver_port, i, ack, frames[i])
            print(f"→ Sent: {segment}")
            receiver_app.receive_segment(segment)

        ack_success = True  # Make deterministic for now
        if ack_success:
            ack = window_end
            seq = window_end
            print("✓ ACK received for all frames.")
        else:
            print("✗ ACK lost. Go back to seq:", seq)

    print("[Transport Layer] Sliding window transmission complete.")
