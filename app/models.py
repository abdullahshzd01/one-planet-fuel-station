from django.db import models
# from django.contrib.auth.models import User
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# class StationManager(BaseUserManager):
#     def create_station(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError('The Email field must be set')

#         email = self.normalize_email(email)
#         station = self.model(email=email, **extra_fields)
#         station.set_password(password)
#         station.save(using=self._db)
#         return station

#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)

#         return self.create_user(email, password, **extra_fields)

# Create your models here.
# class fuelStations(AbstractBaseUser):
class fuelStations(models.Model):
    # station_id = models.IntegerField(auto_created=0)
    name = models.CharField('Station Name', max_length=100)
    address = models.CharField('Station Address', max_length=500)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=15)

    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['first_name', 'last_name']

    # objects = StationManager()

    def __str__(self):
        return self.name

class products(models.Model):
    # prdct_id = models.IntegerField(auto_created=0)
    title = models.CharField(max_length=50, blank=True)
    description = models.TextField()
    category = models.CharField(max_length=35, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='images')
    price = models.FloatField()
    details = models.TextField()
    fuelStation = models.ForeignKey(fuelStations, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class users(models.Model):
    firstName = models.CharField(max_length=50)
    LastName = models.CharField(max_length=50)
    email = models.EmailField(blank=True, unique=True)
    phone = models.CharField(max_length=15)

    def __str__(self):
        # return self.email
        return self.firstName + ' ' + self.LastName

class cart(models.Model):
    # cart_id = models.CharField(max_length=6)
    user = models.ForeignKey(users, blank=True, on_delete=models.CASCADE)
    products = models.ManyToManyField(products, blank=True)

    def __str__(self):
        # return self.cart_id
        return self.user

class jobs(models.Model):
    job_name = models.CharField(max_length=150, null=True, blank=True)
    designation = models.CharField(max_length=100)
    # fuelStation_Name = models.CharField()
    # fuelStation_addrs = models
    # phone_number = 
    fuelStation = models.ForeignKey(fuelStations, blank=True, null=True, on_delete=models.CASCADE)
    details = models.TextField('Job details')

    def __str__(self):
        return self.job_name

class applicant(models.Model):
    job = models.ManyToManyField(jobs, blank=True)
    user = models.ForeignKey(users, blank=True, on_delete=models.CASCADE)
    cv = models.FileField(null=True, blank=True, upload_to="CVs/")

    def __str__(self):
        return self.user.firstName + ' ' + self.user.LastName + ' : ' + self.job.job_name + " Application"

class reviews(models.Model):
    user = models.ForeignKey(users, blank=True, null=True, on_delete=models.CASCADE)
    review = models.TextField()
    rating = models.FloatField()

    def __str__(self):
        return self.user.firstName + ' ' + self.user.LastName

class myAdmin(models.Model):
    email = models.EmailField(blank=True, unique=True)
    password = models.CharField(max_length=15)

    def __str__(self):
        return self.email

class order(models.Model):
    totalCost = models.FloatField()
    # product = models.ManyToOneRel(products)
    Customer = models.ForeignKey(users, blank=True, null=True, on_delete=models.CASCADE)
    orderDate = models.DateField(auto_now_add=True)
    fuelStation = models.ForeignKey(fuelStations, blank=True, null=True, on_delete=models.CASCADE)

    def __date__(self):
        # return str(self.id)
        # return self.orderDate
        return self.orderDate
