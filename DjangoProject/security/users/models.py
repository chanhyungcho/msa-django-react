from django.db import models

class User(models.Model):
    use_in_migrations = True
    user_id = models.AutoField(primary_key=True)
    username = models.TextField()
    password = models.TextField()
    created_at = models.TextField()
    rank = models.IntegerField()
    point = models.IntegerField()

    class Meta:
        db_table = "users"

    def __str__(self):
        return f'{self.pk} {self.username} {self.password} {self.created_at} {self.rank} {self.point}'
