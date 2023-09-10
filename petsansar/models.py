from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Contact(models.Model):
    contact_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    desc = models.TextField(max_length=500)
    phonenumber = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Animal(models.Model):
    animal_id = models.AutoField
    animaltype = models.CharField(max_length=50, default="")
    breeds = models.CharField(max_length=50, default="")
    color = models.CharField(max_length=10, default="")
    eyecolor = models.CharField(max_length=10, default="")
    desc = models.TextField(max_length=100, default="")
    DOB = models.DateField()
    sex = models.CharField(max_length=8, default="")
    weight = models.IntegerField()
    medical_condition = models.CharField(max_length=10, default="")
    location = models.CharField(max_length=50, default="")
    available_for_adoption = models.BooleanField(default=True)
    image = models.ImageField(upload_to='adopt/images')
    adopted = models.BooleanField(default=False)

    def __str__(self):
        return self.breeds


class Surrender(models.Model):
    animal_id = models.AutoField
    animaltype = models.CharField(max_length=50, default="")
    breeds = models.CharField(max_length=50, default="")
    color = models.CharField(max_length=10, default="")
    desc = models.TextField(max_length=100, default="")
    DOB = models.DateField()
    sex = models.CharField(max_length=8, default="")
    weight = models.IntegerField()
    medical_condition = models.CharField(max_length=10, default="")
    medical_certificate=models.ImageField(upload_to="img/%y",blank="True", null="True")
    location = models.CharField(max_length=200, default="")
    is_approved = models.BooleanField(default=False)
    image = models.ImageField(upload_to="img/%y")

    def __str__(self):
        return self.breeds


class Donation(models.Model):
    donation_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    phonenumber = models.IntegerField()
    desc = models.TextField(max_length=500)

    def __str__(self):
        return self.name


class Strayanimal(models.Model):
    strayanimal_id = models.AutoField(primary_key=True)
    description = models.TextField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    image = models.ImageField(upload_to="img/%y")

    def __int__(self):
        return self.id


class RescueLocation(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name


class Strayanimalrescue(models.Model):
    name = models.CharField(max_length=100)
    phone = models.TextField(max_length=10)
    location = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()
    description = models.TextField(max_length=500)
    image = models.ImageField(upload_to="img/%y")
    date_reported = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class AdoptionRequest(models.Model):
    ADOPTION_STATUS = (
        ("pending", "pending"),
        ("rejected", "rejected"),
        ("Accepted", "Accepted"),
        ("Not Available","Not Available"),
    )
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name="adoption_requests")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="adoption_requests")
    contact = models.TextField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    description = models.TextField(max_length=100, null=True, blank=True)
    status = models.CharField(choices=ADOPTION_STATUS, default='pending', max_length=20)

    def __str__(self):
        return f"Adoption Request for {self.animal.breeds}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    adoption_request = models.ForeignKey('AdoptionRequest', on_delete=models.CASCADE)


class ListAdoptionRequest(models.Model):
    ADOPTION_STATUS =(
    ("pending", "pending"),
    ("rejected", "rejected"),
    ("Accepted", "Accepted"),
    ("Not Available","Not Available"),
)
    pet = models.ForeignKey(Surrender, on_delete=models.CASCADE, related_name="list_requests")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="list_requests")
    contact= models.TextField(null=True, blank=True)
    address= models.TextField(null=True, blank=True)
    description = models.TextField(max_length=100, null=True, blank=True)
    status = models.CharField(choices=ADOPTION_STATUS, default='pending', max_length=20)

    def __str__(self):
        return f"adoption Request for {self.pet.breeds}"