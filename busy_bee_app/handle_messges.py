from django.http import HttpResponse
from django.contrib import messages

def handle_response_message(request, message: str):
    messages.success(request, message)
    response = HttpResponse()
    response['HX-Refresh'] = 'true'
    return response

# response = HttpResponse()
#         response['HX-Redirect'] = '/success-url/' # Full page will redirect here
#         return response

# with django-htmx
# python
# from django_htmx.http import HttpResponseClientRedirect

# def your_view(request):
#     if form.is_valid():
#         form.save()
#         return HttpResponseClientRedirect('/success-url/')