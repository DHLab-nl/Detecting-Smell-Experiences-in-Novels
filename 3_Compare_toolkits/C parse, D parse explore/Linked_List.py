class Node:
    def __init__(self, identifier=None, data=None):
        self.identifier = identifier  # node identifier, sought by find_node method
        self.data = data
        self.next_node = None


class LinkedList:
    def __init__(self):
        self.head = None  # references to head and tail nodes
        self.tail = None

    def append(self, identifier, data):
        """Append a new node to the end of linket list object.
        """
        new_node = Node(identifier, data)

        if self.tail:  # one or more nodes already present in linked list
            self.tail.next_node = new_node
            self.tail = new_node
        else:
            self.head = new_node
            self.tail = new_node

    def find_node(self, search_identifier):
        """Return (an alias to) the node whose identifier matches the search.
        Otherwise return false
        """

        current_node = self.head
        while (
            current_node.identifier != search_identifier
            and current_node.next_node is not None
        ):  # don't try to increment beyond tail node
            current_node = current_node.next_node

        if current_node.identifier == search_identifier:  # found a match
            return current_node
        else:
            return False

    def amend_node_data(self, search_identifier, replacement_data):
        """For the node whose identifier matches search_identifier; replace
        data with replacement_data
        """
        target_node = self.find_node(search_identifier)

        if target_node:  # if node found
            target_node.data = replacement_data
        else:
            return False
