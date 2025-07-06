from django.db import models
from django.urls import reverse
from PIL import Image
import os 

class Car(models.Model):
	CONDITION_CHOICES = [
		('excellent', 'Excellent'),
		('good', 'Good'),
		('fair', 'Fair'),
		('poor', 'Poor'),
	]	

	FUEL_TYPE_CHOICES = [
		('gas', 'Gas'),
		('diesel', 'Diesel'),
		('hybrid', 'Hybrid'),
		('electric', 'Electric'),
	]

	TRANSMISSION_CHOICES = [
		('manual', 'Manual'),
		('automatic', 'Automatic'),
	]

	make = models.CharField(max_length=50)
	model = models.CharField(max_length=50)
	year = models.IntegerField()
	mileage = models.IntegerField()
	price = models.DecimalField(max_digits=10, decimal_places=2)

	condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
	fuel_type = models.CharField(max_length=20, choices=FUEL_TYPE_CHOICES)
	transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES)
	exterior_color = models.CharField(max_length=30)
	interior_color = models.CharField(max_length=30)

	vin = models.CharField(max_length=17, unique=True)
	description = models.TextField(blank=True)
	features = models.TextField(blank=True, help_text="List special features, one per line")

	main_image = models.ImageField(upload_to='car_images/', blank=True, null=True)
	image_2 = models.ImageField(upload_to='car_images/', blank=True, null=True)
	image_3 = models.ImageField(upload_to='car_images/', blank=True, null=True)
	image_4 = models.ImageField(upload_to='car_images/', blank=True, null=True)
	image_5 = models.ImageField(upload_to='car_images/', blank=True, null=True)

	is_available = models.BooleanField(default=True)
	is_featured = models.BooleanField(default=False, help_text="Show on homepage")

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-created_at']
		verbose_name = 'Car'
		verbose_name_plural = 'Cars'

	def __str__(self):
		return f"{self.year} {self.make} {self.model}"

	def get_absolute_url(self):
		return reverse('car_detail', kwargs={'pk': self.pk})

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		for field_name in ['main_image', 'image_2', 'image_3', 'image_4', 'image_5']:
			image_field = getattr(self, field_name)
			if image_field:
				self.resize_image(image_field.path)

	def resize_image(self, image_path):
		if os.path.exists(image_path):
			with Image.open(image_path) as img:
				if img.width > 1200 or img.height > 800:
					img.thumbnail((1200,800), Image.Resampling.LANCZOS)
					img.save(image_path, optimize=True, quality=85)

			