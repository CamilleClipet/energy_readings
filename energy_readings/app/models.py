from django.db import models
from django.utils import timezone


class File(models.Model):
    file_name = models.CharField(primary_key=True, max_length=255)
    import_time = models.DateTimeField(default=timezone.now)
    header = models.TextField()
    footer = models.TextField()

    def __str__(self):
        return self.file_name

    class Meta:
        ordering = ["-import_time"]


class Reading(models.Model):
    file_name = models.ForeignKey(File, on_delete=models.CASCADE)
    mpan_core = models.BigIntegerField(null=False)
    validation_status = models.CharField(max_length=1, null=False)
    meter_id = models.CharField(max_length=10, null=False)
    reading_type = models.CharField(max_length=1, null=False)
    meter_register_id = models.CharField(max_length=2, null=False)
    reading_datetime = models.DateTimeField(null=False)
    register_reading = models.FloatField(null=False)
    md_reset_datetime = models.DateTimeField(null=True)
    nb_md_resets = models.IntegerField(null=True)
    meter_reading_flag = models.BooleanField(null=True)
    reading_method = models.CharField(max_length=1, null=False)
    meter_reading_reason_code = models.CharField(max_length=2, null=True)
    meter_reading_status = models.BooleanField(null=True)

    class Meta:
        ordering = ["file_name", "-reading_datetime"]
