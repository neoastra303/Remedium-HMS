from django.db import models

class Ward(models.Model):
    class Meta:
        app_label = 'hospital'

    name = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class Room(models.Model):
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=20)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.ward.name} - Room {self.room_number}'

class Room(models.Model):
    class Meta:
        app_label = 'hospital'

    ward = models.ForeignKey(Ward, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=20)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.ward.name} - Room {self.room_number}'