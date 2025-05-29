from django.db import models
from django.conf import settings

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    basic_brand_credits = models.PositiveIntegerField(default=0)
    filtered_brand_credits = models.PositiveIntegerField(default=0)
    features = models.TextField(null=True, blank=True)
    payment_url = models.URLField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.name


class UserSubscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscriptions")
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, related_name="user_subscriptions")
    remaining_basic_credits = models.PositiveIntegerField(default=0)
    remaining_filtered_credits = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.email} - {self.plan.name}"
