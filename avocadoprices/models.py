from django.db import models

# Create your models here.
class Post(models.Model):
    location_choices = (
        ('HP', 'Hyde Park Produce'),
        ('TG', 'Target'),
        ('TI', 'Treasure Island (RIP)'),
        ('OP', 'Open Produce'),
        ('WF', 'Whole Foods'),
        ('OT', 'Other'),
        ('UK', 'Unknown')
    )

    tweeet_id = models.IntegerField(primary_key=True)
    tweet_published_date = models.DateTimeField()
    tweet_text = models.TextField()
    avocado_price = models.DecimalField(max_digits=4, decimal_places=2)
    avocado_location = models.CharField(
        max_length=20,
        choices=location_choices,
        default='UK'
    )

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
