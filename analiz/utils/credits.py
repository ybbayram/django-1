from ..models import UserSubscription

def deduct_basic_credits(user, count):
    """
    Kullanıcının basic kredi bakiyesini kontrol eder ve yeterliyse düşer.
    """
    subscription = UserSubscription.objects.filter(user=user).first()
    if subscription and subscription.remaining_basic_credits >= count:
        subscription.remaining_basic_credits -= count
        subscription.save()
        return True
    return False

def deduct_filtered_credits(user, count):
    """
    Kullanıcının filtreli sorgu kredi bakiyesini kontrol eder ve yeterliyse düşer.
    """
    subscription = UserSubscription.objects.filter(user=user).first()
    if subscription and subscription.remaining_filtered_credits >= count:
        subscription.remaining_filtered_credits -= count
        subscription.save()
        return True
    return False
