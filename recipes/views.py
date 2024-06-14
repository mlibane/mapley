from django.shortcuts import render

# Define the main view function
def main(request):
    # Render the main.html template
    return render(request, 'recipes/main.html')

def recipes(request):
    return None