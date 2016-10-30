from django.conf import settings
from django.utils import timezone
settings.configure(settings)
print(timezone.now())
