from django.contrib import admin
from django.utils.html import format_html
from .models import Car, Contact

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
		return "No Image"
	image_preview.short_description = "Preview"

	actions = ['mark_as_sold', 'mark_as_available', 'mark_as_featured']

	def mark_as_sold(self, request, queryset):
		queryset.update(is_available=False)
		self.message_user(request, f"{queryset.account()} cars marked as sold.")
	mark_as_sold.short_description = "Mark selected cars as sold"

	def mark_as_available(self, request, queryset):
		queryset.update(is_available=True)
		self.message_user(request, f"{queryset.count()} cars marked as available")
	mark_as_available.short_description = "Mark selecte cars as available"

	def mark_as_featured(self, request, queryset):
		queryset.update(is_featured=True)
		self.message_user(request, f"{queryset.count()} cars marked as featured.")
	mark_as_featured.short_description = "Mark selected cars as featured"


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
	list_display = ['name', 'email', 'phone', 'subject_display', 'created_at', 'is_resolved']
	list_filter = ['subject', 'is_resolved', 'created_at']
	search_fields = ['name', 'email', 'phone']
	liste_editable = ['is_resolved']
	readonly_fields = ['created_at']
	date_hierarchy = 'created_at'

	fieldsets = (
		('Contact Information', {
			'fields': ('name', 'email','phone')
			}),
		('Inquiry Details', {
			'fields': ('subject', 'message')
			}),
		('Status', {
			'fields': ('is_resolved', 'created_at')
			}),
	)

	def subject_display(self, obj):
		return obj.get_subject_display()
	subject_display.short_description = 'Subject'

	actions = ['mark_as_resolved', 'mark_as_unresolved']

	def mark_as_resolved(self, request, queryset):
		queryset.update(is_resolved=True)
		self.message_user(request, f"{queryset.count()} inquiries marked as resolved")
	mark_as_resolved.short_description = "Mark selected inquiries as resolved"

	def mark_as_unresolved(self, request, queryset):
		queryset.update(is_resolved=False)
		self.message_user(request, f"{queryset.count()} inquiries marked as unresolved.")
	mark_as_unresolved.short_description = "Mark selected inquiries as unresolved"