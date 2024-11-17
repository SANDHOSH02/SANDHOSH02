import threading
import random
import time
import logging
from colorama import init, Fore, Back, Style
from prettytable import PrettyTable

# Initialize colorama
init(autoreset=True)

# Set up logging with a custom formatter to limit output
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

class DistributedSystemNode:
    def __init__(self, node_name):
        self.node_name = node_name
        self.state = 0
        self.neighbors = []
        self.received_snapshots = set()
        self.lock = threading.Lock()
        self.recording_state = False
        self.state_snapshots = {}

    def send_message(self, receiver_node, message):
        logger.info(Fore.CYAN + f"{self.node_name} sends message '{message}' to {receiver_node.node_name}")
        receiver_node.receive_message(self.node_name, message)

    def receive_message(self, sender_name, message):
        with self.lock:
            if message == 'SNAPSHOT_MARKER':
                self.handle_snapshot_marker(sender_name)
            else:
                logger.info(Fore.GREEN + f"{self.node_name} received message '{message}' from {sender_name}")
                if self.recording_state:
                    self.state_snapshots.setdefault(sender_name, []).append(message)

    def handle_snapshot_marker(self, sender_name):
        if not self.recording_state:
            logger.info(Fore.YELLOW + f"{self.node_name} starts recording its state")
            self.recording_state = True
            self.state_snapshots['self'] = self.state
            for neighbor in self.neighbors:
                neighbor.send_snapshot_marker()
        else:
            logger.info(Fore.YELLOW + f"{self.node_name} received snapshot marker from {sender_name} (already recording)")
        self.received_snapshots.add(sender_name)

    def send_snapshot_marker(self):
        for neighbor in self.neighbors:
            logger.info(Fore.MAGENTA + f"{self.node_name} sends snapshot marker to {neighbor.node_name}")
            neighbor.receive_message(self.node_name, 'SNAPSHOT_MARKER')

    def simulate_activity(self):
        while True:
            time.sleep(random.randint(1, 3))
            self.state += random.randint(1, 5)
            if self.neighbors:
                receiver = random.choice(self.neighbors)
                self.send_message(receiver, f"State update {self.state}")
            self.print_node_status()

    def print_node_status(self):
        """Print the node's status in a table."""
        table = PrettyTable()
        table.field_names = ["Node", "State", "Recording State"]
        table.add_row([self.node_name, self.state, "Yes" if self.recording_state else "No"])
        logger.info(Fore.WHITE + str(table))

def initialize_system(num_nodes=3):
    nodes = [DistributedSystemNode(f"Node {i}") for i in range(num_nodes)]
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            if i != j:
                nodes[i].neighbors.append(nodes[j])
    return nodes

def start_simulation(nodes):
    threads = []
    for node in nodes:
        thread = threading.Thread(target=node.simulate_activity)
        thread.start()
        threads.append(thread)
    return threads

def main():
    nodes = initialize_system()
    threads = start_simulation(nodes)
    time.sleep(5)
    logger.info(Fore.RED + "Starting snapshot process from Node 0")
    nodes[0].send_snapshot_marker()
    time.sleep(10)
    for thread in threads:
        thread.join(timeout=1)

if __name__ == "__main__":
    main()
