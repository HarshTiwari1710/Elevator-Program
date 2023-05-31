# views.py
from rest_framework import viewsets
from .models import Elevator, Request
from .serializers import ElevatorSerializer, RequestSerializer
from .Elevatorlogic import ElevatorLogic, UP_Button, DOWN_Button
from rest_framework.response import Response

class ElevatorViewSet(viewsets.ModelViewSet):
    queryset = Elevator.objects.all()
    serializer_class = ElevatorSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Get the elevator logic instance for the current elevator
        elevator_logic = ElevatorLogic(callbacks=instance)

        # Update the elevator logic based on the request data
        if 'destination_floor' in request.data:
            elevator_logic.on_floor_selected(request.data['destination_floor'])

        if 'motor_direction' in request.data:
            motor_direction = request.data['motor_direction']
            if motor_direction == UP_Button:
                elevator_logic.callbacks.motor_direction = UP_Button
            elif motor_direction == DOWN_Button:
                elevator_logic.callbacks.motor_direction = DOWN_Button
            else:
                elevator_logic.callbacks.motor_direction = None

        # Call the on_ready method to trigger elevator movement
        elevator_logic.on_ready()

        # Save the updated elevator state
        serializer.save()

        return Response(serializer.data)

