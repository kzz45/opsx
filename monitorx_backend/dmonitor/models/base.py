import time
from django.db import models


def now_ts():
    return int(time.time())


class BaseModel(models.Model):
    class Meta:
        abstract = True

    id = models.AutoField(primary_key=True, unique=True)
    create_at = models.IntegerField(default=now_ts, verbose_name="创建时间")
    update_at = models.IntegerField(default=now_ts, verbose_name="更新时间")

    def save(self, *args, **kwargs):
        self.update_at = now_ts()
        super(BaseModel, self).save(*args, **kwargs)
