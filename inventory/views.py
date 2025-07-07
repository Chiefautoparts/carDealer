from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Car
from .forms import ContactForm

def home(request):
	"""Homepage showing featured cars"""
	featured_cars = Car.objects.filter(is_available=True, is_featured=True)[:6]
	recent_cars = Car.objects.filter(is_available=True)[:8]

	context = {
		'featured_cars': featured_cars,
		'recent_cars': recent_cars,
	}
	return render(request, 'inventory/home.html', context)

def inventory(request):
	"""Show all available cars with filtering"""
	cars = Car.objects.filter(is_available=True)

	# Filter by search query
	search_query = request.GET.get('search')
	if search_query:
		cars = cars.filter(
			Q(make__icontains=search_query) |
			Q(model__icontains=search_query) |
			Q(year__icontains=search_query)
		)

	# Filter by make
	make_filter = request.GET.get('make')
	if make_filter:
		cars = cars.filter(make__iexact=make_filter)

	# Filter by price range
	min_price = request.GET.get('min_price')
	max_price = request.GET.get('max_price')
	if min_price:
		cars = cars.filter(price__gte=min_price)
	if max_price:
		cars = cars.filter(price__lte=max_price)

	# Filter by year range
	min_year = request.GET.get('min_year')
	max_year = request.GET.get('max_year')
	if min_year:
		cars = cars.filter(year__gte=min_year)
	if max_year:
		cars = cars.filter(year__lte=max_year)


	paginator = Paginator(cars, 12)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	available_makes = Car.objects.filter(is_available=True).values_list('make', flat=True).distinct().order_by('make')

	context = {
		'page_obj': page_obj,
		'available_makes': available_makes,
		'current_filters': request.GET,
	}
	return render(request, 'inventory/inventory.html', context)

def car_detail(request, pk):
	"""Show detailed view of a single car"""
	car = get_object_or_404(Car, pk=pk, is_available=True)

	images = []
	for field_name in ['main_image', 'image_2', 'image_3', 'image_4', 'image_5']:
		image_field = getattr(car, field_name)
		if image_field:
			images.append(image_field.url)

	features = []
	if car.features:
		features = [features.strip() for features in car.features.split('\n') if feature.strip()]

	context = {
		'car': car,
		'images': images,
		'features': features,
	}
	return render(request, 'inventory/car_detail.html', context)

def contact(request):
	"""Contact page with form"""
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			name = form.cleaned_data['name']
			email = form.cleaned_data['email']
			phone = form.cleaned_data['phone']
			subject = form.cleaned_data['subject']
			message = form.cleaned_data['message']

			department_emails = {
				'general': 'info@autosales.com',
                'sales': 'sales@autosales.com',
                'service': 'service@autosales.com',
                'financing': 'financing@autosales.com',
                'trade_in': 'tradein@autosales.com',
                'parts': 'parts@autosales.com',
			}

			department_email = department_emails.get(subject, 'info@autosales.com')

			subject_display = dict(form.fields['subject'].choices[subject])
			email_subject - f"Website Contact: {subject_display} - {name}"

			email_message = f"""
New contact form submission:

Name: {name}
Email: {email}
Phone: {phone}
Subject: {subject_display}

Message:
{message}

---
This message was sent from the Auto Sales website contact form.
            """

             try:
                # Send email to department
                send_mail(
                    subject=email_subject,
                    message=email_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[department_email],
                    fail_silently=False,
                )
                
                # Send confirmation email to customer
                confirmation_subject = "Thank you for contacting Auto Sales"
                confirmation_message = f"""
Dear {name},

Thank you for contacting Auto Sales. We have received your message regarding "{subject_display}" and will get back to you within 24 hours.

Our {subject_display.lower()} team will review your inquiry and respond to you at {email} or call you at {phone}.

Best regards,
Auto Sales Team

---
This is an automated confirmation email.
                """
                
                send_mail(
                    subject=confirmation_subject,
                    message=confirmation_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=True,  # Don't fail if customer email fails
                )
                
                messages.success(request, 'Thank you for your message! We will contact you within 24 hours.')
                form = ContactForm()  # Reset form
                
            except Exception as e:
                messages.error(request, 'Sorry, there was an error sending your message. Please try again or call us directly.')
    else:
    	form = ContactForm()

    return render(request, 'inventory/contact.html', {'form': form})

    