"""
node class:

Used to create an API instance to interact with the tangle
"""

from iota import Iota
from iota.adapter.wrappers import RoutingWrapper
import requests


class Node:

    def __init__(self, seed, iota_node, route_pow=False, pow_node=''):

        # Node variables
        self.iota_node = iota_node  # Public node
        self.pow_node = pow_node  # Local node to perform PoW

        # Creates an Iota API
        self.api = self.create_api(seed, route_pow)

    def create_api(self, seed, route_pow) -> Iota:
        """Creates an Iota object to interact with the tangle

        :param seed: The seed of the device
        :param route_pow: Boolean to state whether PoW is outsourced
        :return: An Iota object
        """
        try:
            if route_pow is True:
                self.api = \
                    Iota(
                        RoutingWrapper(self.iota_node)
                            .add_route('attachToTangle', self.pow_node)
                            .add_route('interruptAttachingToTangle', self.pow_node),
                        seed=seed
                    )
            else:
                self.api = Iota(self.iota_node, seed)

                # Uncomment to test node after creating an API
                # self.test_node()
            return self.api

        except ConnectionRefusedError as e:
            print(e)
            print("Ensure all nodes are working correctly before connecting")

    def test_node(self):
        """Tests the connection to the node and if it is synced
        """
        try:
            status = self.api.get_node_info()
            print("Successfully connected to IOTA Node!")
            if abs(status['latestMilestoneIndex'] - status['latestSolidSubtangleMilestoneIndex']) > 3:
                print("\rIota node is not synced!")
            else:
                print("\rIota node is synced!")
        except requests.exceptions.ConnectionError:
            print("Connection refused")
