from django.db import models


class Elevator(models.Model):
    STATUS_CHOICES = (
        ('operational', 'Operational'),
        ('maintenance', 'Maintenance')
    )

    DIRECTION_CHOICES = (
        ('up', 'Up'),
        ('down', 'Down'),
        ('stopped', 'Stopped')
    )

    current_floor = models.PositiveIntegerField()
    direction = models.CharField(max_length=10, choices=DIRECTION_CHOICES, default='stopped')
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='operational')


class Request(models.Model):
    elevator = models.ForeignKey(Elevator, on_delete=models.CASCADE, related_name='requests')
    floor = models.PositiveIntegerField()
