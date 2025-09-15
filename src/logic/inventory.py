from .order import Order

class Node:
    def __init__(self, order: Order):
        self.order = order
        self.next = None
        self.prev = None


class Inventory:
    def __init__(self, peso_maximo=10):
        self.first = None
        self.last = None
        self.current_order = None
        self.max_weight = peso_maximo
        self.current_weight = 0
        self.order_count = 0

    def add_order(self, order: Order):
        if self.current_weight + order.weight > self.max_weight:
            raise ValueError(f"Cannot add {order.id}. Exceeds maximum weight.")

        new_node = Node(order)
        if self.first is None:
            self.first = new_node
            self.last = new_node
            self.current_order = new_node
        else:
            self.last.next = new_node
            new_node.prev = self.last
            self.last = new_node

        self.current_weight += order.weight
        self.order_count += 1
        print(f"Order {order.id} added to inventory.")
        return True

    def view_next_order(self):
        if self.current_order and self.current_order.next:
            self.current_order = self.current_order.next
            print(f"Viewing order: {self.current_order.order.id}")
        else:
            print("Already at the last order.")

    def view_prev_order(self):
        if self.current_order and self.current_order.prev:
            self.current_order = self.current_order.prev
            print(f"Viewing order: {self.current_order.order.id}")
        else:
            print("Already at the first order.")

    def complete_current_order(self):
        if self.current_order is None:
            print("No order selected to complete.")
            return

        completed_order = self.current_order.order

        if self.current_order.prev:
            self.current_order.prev.next = self.current_order.next
        else:
            self.first = self.current_order.next

        if self.current_order.next:
            self.current_order.next.prev = self.current_order.prev
        else:
            self.last = self.current_order.prev

        if self.current_order.next:
            self.current_order = self.current_order.next
        else:
            self.current_order = self.current_order.prev

        self.current_weight -= completed_order.weight
        self.order_count -= 1
        print(f"Order {completed_order.id} completed!")
        return completed_order

    def sort_inventory(self, key):
        """
        Sorts the inventory in-place in descending order according to the provided key function.

        Args:
            key (callable): A function that takes an Order object and returns a value to sort by (e.g., lambda o: o.weight).
        """
        if not self.first or not self.first.next:
            print("Inventory is already sorted or empty.")
            return
        """
        The sorting is done in descending order.
        """
        if not self.first or not self.first.next:
            print("Inventory is already sorted or empty.")
            return

        # Save the current order's id to restore the pointer after sorting
        current_id = self.current_order.order.id if self.current_order else None

        sorted_head = None
        current = self.first

        # Perform insertion sort on the linked list
        while current:
            next_to_process = current.next
            current.prev = None
            current.next = None

            # Insert at the beginning if sorted_head is None or current's key is greater
            if (sorted_head is None or
                key(current.order) > key(sorted_head.order)):
                current.next = sorted_head
                if sorted_head:
                    sorted_head.prev = current
                sorted_head = current
            else:
                # Find the correct position to insert current node
                seeker = sorted_head
                while (seeker.next and
                       key(seeker.next.order) >= key(current.order)):
                    seeker = seeker.next

                current.next = seeker.next
                if seeker.next:
                    seeker.next.prev = current
                seeker.next = current
                current.prev = seeker

            current = next_to_process

        # Update first and last pointers
        self.first = sorted_head
        last_node = self.first
        while last_node.next:
            last_node = last_node.next
        self.last = last_node

        # Restore the current_order pointer
        if current_id is not None:
            node = self.first
            while node:
                if node.order.id == current_id:
                    self.current_order = node
                    break
                node = node.next

        print("Inventory sorted.")
