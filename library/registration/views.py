from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

# DECORATORS
from django.utils.decorators import method_decorator
from .decorators import logout_required

@method_decorator(logout_required, name='dispatch')
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'