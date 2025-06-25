from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.urls import reverse
from django.db import models
from .models import Tool
from .forms import ToolForm


def home(request):
    tools = Tool.objects.all().order_by('-created_at')

    category = request.GET.getlist('category')
    borrowed_by = request.GET.getlist('borrowed_by')
    borrow_date = request.GET.get('borrow_date', '')
    search = request.GET.get('search', '')
    sort_borrow_date = request.GET.get('sort_borrow_date', '')

    if category:
        tools = tools.filter(category__in=category)
    if borrowed_by:
        tools = tools.filter(borrowed_by__in=borrowed_by)
    if borrow_date:
        tools = tools.filter(borrow_date=borrow_date)
    if search:
        tools = tools.filter(
            models.Q(name__icontains=search) |
            models.Q(barcode__icontains=search) |
            models.Q(location__icontains=search) |
            models.Q(description__icontains=search) |
            models.Q(category=search) |
            models.Q(borrowed_by=search)
        )

    if sort_borrow_date == 'asc':
        tools = tools.order_by('borrow_date')
    elif sort_borrow_date == 'desc':
        tools = tools.order_by('-borrow_date')

    # For filter dropdowns
    categories = Tool.objects.values_list('category', flat=True).distinct()
    borrowers = Tool.objects.values_list('borrowed_by', flat=True).distinct()
    locations = Tool.objects.values_list('location', flat=True).distinct()

    return render(request, 'home.html', {
        'tools': tools,
        'categories': categories,
        'borrowers': borrowers,
        'locations': locations,
        'selected_category': category,
        'selected_borrowed_by': borrowed_by,
        'selected_borrow_date': borrow_date,
        'search': search,
        'selected_location': request.GET.getlist('location'),
        'sort_borrow_date': sort_borrow_date,
    })

def add_tool(request):
  if request.method == 'POST':
      form = ToolForm(request.POST)
      if form.is_valid():
          form.save()
          messages.success(request, 'Tool added successfully!')
          return redirect('home')
      else:
          messages.error(request, 'Error adding tool.')
  else:
      form = ToolForm()
  
  borrowers = Tool.objects.values_list('borrowed_by', flat=True).distinct()
  categories = Tool.objects.values_list('category', flat=True).distinct()
  locations = Tool.objects.values_list('location', flat=True).distinct()
  return render(request, 'tool_form.html', {'form': form, 'title': 'Add Tool', 'borrowers': borrowers, 'categories': categories, 'locations': locations})

def edit_tool(request, pk):
  tool = get_object_or_404(Tool, id=pk)
  if request.method == 'POST':
      form = ToolForm(request.POST, instance=tool)
      if form.is_valid():
          form.save()
          messages.success(request, 'Tool updated successfully!')
          return redirect('home')
      else:
          messages.error(request, 'Error updating tool.')
  else:
      form = ToolForm(instance=tool)
  
  categories = Tool.objects.values_list('category', flat=True).distinct()
  borrowers = Tool.objects.values_list('borrowed_by', flat=True).distinct()
  locations = Tool.objects.values_list('location', flat=True).distinct()
  return render(request, 'tool_form.html', {'form': form, 'title': 'Edit Tool', 'tool': tool, 'categories': categories, 'borrowers': borrowers, 'locations': locations})

def delete_tool(request, pk):
  tool = get_object_or_404(Tool, id=pk)
  tool.delete()
  messages.success(request, 'Tool deleted successfully!')
  return redirect('home')

def scan_barcode(request):
  return render(request, 'scan.html')

@csrf_exempt
def save_barcode(request):
    if request.method == 'POST':
        barcode_data = request.POST.get('barcode_data', None)
        if barcode_data:
            try:
                tool = Tool.objects.get(barcode=barcode_data)
                return JsonResponse({
                    'status': 'success', 
                    'message': 'Tool found!', 
                    'existing_item': True,
                    'tool_id': tool.id,
                    'tool_name': tool.name or 'Unnamed Tool'
                })
            except Tool.DoesNotExist:
                return JsonResponse({
                    'status': 'success', 
                    'message': 'Tool not found. Please add it first.', 
                    'existing_item': False
                })
        else:
            return JsonResponse({'status': 'error', 'message': 'No barcode data received'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

def find_tool_by_barcode(request, barcode):
    try:
        tool = Tool.objects.get(barcode=barcode)
        return redirect('edit_tool', pk=tool.id)
    except Tool.DoesNotExist:
        messages.error(request, f'No tool found with barcode: {barcode}')
        return redirect('home')

def tool_detail(request, pk):
    tool = get_object_or_404(Tool, id=pk)
    return render(request, 'tool_detail.html', {'tool': tool})