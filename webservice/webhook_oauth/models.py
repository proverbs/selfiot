from django.db import models

class Device(models.Model):
    # Device information
    externalDeviceId = models.CharField(max_length=50, unique=True)
    # deviceCookie = models.CharField(max_length=100)
    friendlyName = models.CharField(max_length=50)
    deviceHandlerType = models.CharField(max_length=50)

    class Meta:
        db_table = "device_info"

    def __str__(self):
        return self.friendlyName


class Manufacturer(models.Model):
    # Device manufacturer information
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    manufacturerName = models.CharField(max_length=50)
    modelName = models.CharField(max_length=50)
    hwVersion = models.CharField(max_length=50, default="", blank=True)
    swVersion = models.CharField(max_length=50, default="", blank=True)
    
    class Meta:
        db_table = "device_manufacturer"

    def __str__(self):
        return self.manufacturerName


class Context(models.Model):
    # Device context
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    roomName = models.CharField(max_length=50, default="", blank=True)
    groups = models.CharField(max_length=50, default="", blank=True)
    categories = models.CharField(max_length=50, default="", blank=True)

    class Meta:
        db_table = "device_context"

    def __str__(self):
        return self.roomName


class State(models.Model):
    # Device state information
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    component = models.CharField(max_length=50)
    capability = models.CharField(max_length=50)
    attribute = models.CharField(max_length=50)
    value = models.CharField(max_length=50)

    class Meta:
        db_table = "device_states"

    def __str__(self):
        return self.capability

        

