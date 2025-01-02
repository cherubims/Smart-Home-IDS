from django.db import models

class NetworkTraffic(models.Model):
    duration = models.IntegerField(null=False, blank=True)
    protocol_type = models.CharField(max_length=20)
    service = models.CharField(max_length=50)
    flag = models.CharField(max_length=10)
    src_bytes = models.PositiveIntegerField()
    dst_bytes = models.PositiveIntegerField()
    land = models.BooleanField()
    wrong_fragment = models.PositiveIntegerField()
    urgent = models.PositiveIntegerField()
    hot = models.PositiveIntegerField()
    logged_in = models.BooleanField()
    num_compromised = models.PositiveIntegerField()
    count = models.PositiveIntegerField()
    srv_count = models.PositiveIntegerField()
    serror_rate = models.FloatField()
    rerror_rate = models.FloatField()
    same_srv_rate = models.FloatField()
    diff_srv_rate = models.FloatField()
    srv_diff_host_rate = models.FloatField()
    dst_host_count = models.PositiveIntegerField()
    dst_host_srv_count = models.PositiveIntegerField()
    dst_host_same_srv_rate = models.FloatField()
    dst_host_diff_srv_rate = models.FloatField()
    attack = models.BooleanField()  # True for 'Yes', False for 'No'

    def __str__(self):
        return f"{self.protocol_type} - {self.service} - Attack: {self.attack}"
