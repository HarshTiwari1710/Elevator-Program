from collections import deque

UP_Button = 1
DOWN_Button = 2
FLOOR_COUNT = 6

class ElevatorLogic(object):
    def __init__(self):
        self.destination_floor = None
        self.callbacks = None
        self.requests = deque()  # Queue to store elevator requests

    def on_called(self, floor, direction):
        self.requests.append((floor, direction))  # Add the new request to the queue

        # If the elevator is not moving, process the request immediately
        if self.callbacks.motor_direction is None:
            self.process_request()

    def on_floor_selected(self, floor):
        self.requests.append((floor, None))  # Add the new destination floor to the queue

        # If the elevator is not moving, process the request immediately
        if self.callbacks.motor_direction is None:
            self.process_request()

    def on_floor_changed(self):
        if self.destination_floor == self.callbacks.current_floor:
            self.callbacks.motor_direction = None

            # Process the next request in the queue
            if self.requests:
                self.process_request()

    def on_ready(self):
        # If there are pending requests, process the next request in the queue
        if self.requests:
            self.process_request()

    def process_request(self):
        # Pop the next request from the queue
        floor, direction = self.requests.popleft()

        # Determine the motor direction based on the request
        if floor > self.callbacks.current_floor:
            self.callbacks.motor_direction = UP_Button
        elif floor < self.callbacks.current_floor:
            self.callbacks.motor_direction = DOWN_Button
        else:
            self.callbacks.motor_direction = None

        self.destination_floor = floor
