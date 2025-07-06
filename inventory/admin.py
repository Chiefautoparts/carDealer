from django.contrib import admin
from django.utils.html import format_html
from .models import Car

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'price', 'mileage', 'condition', 'is_available', 'is_featured', 'image_preview']
	list_filter = ['make', 'year', 'condition', 'fuel_type', 'transmission', 'is_available', 'is_featured']
	search_fields = ['make', 'model', 'vin', 'year']
	list_editable = ['is_available', 'is_featured', 'price']

	fieldsets =(
		('Basic Information', {
			'fields': ('make', 'model', 'year', 'mileage', 'price', 'vin')
			}),
		('Vehicle Details', {
			'fields': ('condition', 'fuel_type', 'transmission', 'exterior_color', 'interior_color')
			}),
		('Description & Features', {
			'fields': ('description', 'features')
			}),
		('Images', {
			'fields': ('main_image', 'image_2', 'image_3', 'image_4', 'image_5'),
			'classes': ('collapse',)
			}),
		('Status', {
			'fields': ('is_available', 'is_featured')
			}),
		)

	readonly_fields = ['created_at', 'updated_at']

	def image_preview(self, obj):
		if obj.main_image:
			return format_html('<img src="{}" style="width: 50px; height:50px; object-fit: cover;" />', obj.main_image.url)
			