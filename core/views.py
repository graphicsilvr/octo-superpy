from django.shortcuts import render
# comment this out for a second:
# from modules.inventory import get_inventory 

def dashboard(request):
    # Dummy data for testing
    inventory_data = [
        {'name': 'Apple', 'count': 10},
        {'name': 'Orange', 'count': 5},
    ]
    
    context = {
        'inventory': inventory_data,
        'status': 'System Operational'
    }
    return render(request, 'core/dashboard.html', context)