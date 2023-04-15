from django.contrib import admin
from .models import fuelStations
from .models import products
from .models import users
from .models import cart
from .models import jobs
from .models import reviews
from .models import applicant
from .models import myAdmin
from .models import order

# Register your models here.
admin.site.register(fuelStations)
admin.site.register(products)
admin.site.register(users)
admin.site.register(cart)
admin.site.register(jobs)
admin.site.register(reviews)
admin.site.register(applicant)
admin.site.register(myAdmin)
admin.site.register(order)
