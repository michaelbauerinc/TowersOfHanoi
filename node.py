class Node:
    def __init__(self, value, next_node=None):
        self.value = value
        self.next_node = next_node
        self.previous_node = None

    def set_next_node(self, next_node):
        self.next_node = next_node

    def get_next_node(self):
        return self.next_node

    def set_previous_node(self, previous_node):
        self.previous_node = previous_node

    def get_previous_node(self):
        return self.previous_node

    def get_value(self):
        return self.value

    def assign_image(self, image):
        self.image = image

    def get_image(self):
        return self.image