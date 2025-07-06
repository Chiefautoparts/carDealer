from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Car

def home(request):
	"""Homepage showing featured cars"""
	featured_cars = Car.objects.filter(is_available=True, is_featured=True)[:6]
	recent_cars = Car.objects.filter(is_available=True)[:8]

	context = {
		'featured_cars': featured_cars,
		'recent_cars': recent_cars,
	}
	return render(request, 'cars/home.html', context)

def inventory(request):
	"""Show all available cars with filtering"""
	cars = Car.objects.filter(is_available=True)

	search_query = request.GET.get('search')
	if search_query:
		cars = cars.filter(
			Q(make__icontains=search_query) |
			Q(model__icontains=search_query) |
			Q(year__icontains=search_query)
		)

	make_filter = request.GET.get('make')
	if make_filter:
		cars = cars.filter(make__iexact=make_filter)

	min_price = request.GET.get('min_price')
	max_price = request.GET.get('max_price')
	if min_price:
		cars = cars.filter(price__gte=min_price)
	if max_price:
		cars = cars.filter(price__lte=max_price)

	paginator = Paginator(cars, 12)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	available_makes = Car.objects.filter(is_available=True).values_list('make', flat=True).distinct().order_by('make')

	context = {
		'page_obj': page_obj,
		'available_makes': available_makes,
		'current_filters': request.GET,
	}
	return render(request, 'cars/inventory.html', sontext)

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
	return render(request, 'cars/car_detail.html', context)

	