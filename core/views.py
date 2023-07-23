# Imports
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.views import View
from django.views.generic import (ListView,
                                  CreateView,
                                  TemplateView,
                                  DeleteView,
                                  UpdateView)
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView

# Local imports
from core.models import Artist, Design, Appointment
from .forms import (RegisterForm,
                    LoginForm,
                    EditProfileForm,
                    PasswordChangeForm,
                    AppointmentForm)

# Questions and answers for FAQ page
faqs = [
    {
        "question": "Is it safe to get a tattoo at your salon?",
        "answer": "Absolutely! Safety is our top priority. We adhere "
                  "to strict hygiene standards and use only single-use, "
                  "sterilized equipment. Our artists are licensed "
                  "professionals, ensuring a safe and clean environment "
                  "for all our clients."
    },
    {
        "question": "What should I consider before getting a tattoo?",
        "answer": "Before getting a tattoo, think about the design, size, "
                  "and placement carefully. Research our artists' portfolios "
                  "and communicate your ideas with them to ensure your vision "
                  "comes to life. Additionally, consider the aftercare "
                  "requirements and the commitment involved in having"
                  " a tattoo."
    },
    {
        "question": "Can I bring my own design, or do you offer custom"
                    " designs?",
        "answer": "Both options are available! You can bring your design, and "
                  "our skilled artists can adapt it to your preferences"
                  " and body placement. Alternatively, our artists can create "
                  "custom designs tailored specifically to your ideas and"
                  " desires."
    },
    {
        "question": "How much will my tattoo cost?",
        "answer": "Tattoo prices vary depending on size, complexity, "
                  "and the time it takes to complete. During your "
                  "consultation, our artists will provide an accurate "
                  "estimate based on your design and requirements."
    },
    {
        "question": "Do tattoos hurt?",
        "answer": "The level of pain varies from person to person, "
                  "as everyone has a different pain tolerance. "
                  "Generally, tattoos can be uncomfortable, but "
                  "many people find the experience manageable and "
                  "well worth the result."
    },
    {
        "question": "Do you offer tattoo removal services?",
        "answer": "As of now, we don't offer tattoo removal "
                  "services. Our expertise lies in creating "
                  "beautiful tattoos that you'll cherish for a "
                  "lifetime. If you're interested in removal options,"
                  " we can recommend specialized clinics or professionals."
    },
    {
        "question": "Is there an age restriction for getting a tattoo?",
        "answer": "Yes, you must be at least 18 years old to get a tattoo"
                  " without parental consent. We require a valid ID to "
                  "confirm your age before proceeding with any"
                  " tattoo services."
    },
    {
        "question": "How should I take care of my new tattoo?",
        "answer": "Aftercare is crucial for proper healing and to "
                  "maintain the quality of your tattoo. We'll provide you"
                  " with detailed aftercare instructions after your session "
                  "to ensure your tattoo heals perfectly."
    }
]


# Class for home page view
class HomeView(View):
    def get(self, request):
        artists = Artist.objects.all()
        return render(request, 'index.html', context={"artists": artists})


# Class for artists page view
class ArtistView(ListView):
    model = Artist
    template_name = 'artists.html'
    context_object_name = 'artists'


# Class for styles page view
class DesignsView(View):
    def get(self, request):
        designs = Design.objects.all()
        size = ['large', "medium", "small"]
        return render(request, 'styles.html',
                      context={'size': size, "designs": designs})


# Class for FAQ page view
class FAQView(View):
    def get(self, request):
        return render(request, 'faq.html', context={"faqs": faqs})


# Class for registration
# https://dev.to/earthcomfy/creating-a-django-registration-login-app-part-i-1di5
class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})


# Class for login
# https://dev.to/earthcomfy/creating-a-django-registration-login-app-part-i-1di5
class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            self.request.session.set_expiry(0)

            self.request.session.modified = True

        return super(CustomLoginView, self).form_valid(form)


# Class for logout
class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, "You have successfully logged out")
        return redirect('home')


# Class for edit profile
class EditProfileView(LoginRequiredMixin, View):
    login_url = '/login/?next=/edit_profile'

    def get(self, request):
        user = request.user
        if not user:
            return redirect('login')
        profile = EditProfileForm(initial={
                                  'first_name': user.first_name,
                                  'last_name': user.last_name})
        username = request.user.username
        context = {'profile': profile}
        return render(request, 'edit_profile.html', context)

    def post(self, request):
        user = request.user
        if not user:
            return redirect('login')
        form = EditProfileForm(request.POST or None, instance=user)

        if form.is_valid():
            # Update the user data and save the changes
            user = request.user
            if request.method == 'POST':
                if form.is_valid():
                    user.first_name = form.cleaned_data['first_name']
                    user.last_name = form.cleaned_data['last_name']
                    form.save()
                    messages.success(request,
                                     "Your profile has "
                                     "been successfully updated!")
                    return redirect('home')
        else:
            messages.error(request, "Please provide valid information")
            return redirect('edit_profile')
        context = {'form': form}
        return render(request, 'edit_profile.html', context)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please log in to edit profile.')
        return super().dispatch(request, *args, **kwargs)


# Class for password change
class PasswordChangeView(LoginRequiredMixin, View):
    login_url = '/login/?next=/edit_password'

    def get(self, request):
        user = request.user
        if not user:
            return redirect('login')
        change_password = PasswordChangeForm(user)
        context = {"change_password": change_password}
        return render(request, 'edit_password.html', context)

    def post(self, request):
        user = request.user
        if not user:
            return redirect('login')
        change_password = PasswordChangeForm(request.user, request.POST)

        if change_password.is_valid():

            user = change_password.save()
            print(user.password)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(
                request, 'Your password has been successfully updated.')
            change_password.cleaned_data['old_password'] = None
            # Redirect to the same page after successful password change
            return redirect('home')
        else:
            messages.error(request,
                           'Please provide your old '
                           'password and confirm the new one')

        context = {"change_password": change_password}
        return render(request, 'edit_password.html', context)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please log in to change password.')
        return super().dispatch(request, *args, **kwargs)


# Class for appointment booking
class CreateAppointmentView(LoginRequiredMixin, View):
    template_name = 'appointment_form.html'
    login_url = '/login/?next=/appointment/create/'

    def get(self, request, artist_id=None):
        form = AppointmentForm()
        if artist_id is not None:

            form.fields['artist'].initial = artist_id

        return render(request, 'appointment_form.html', {'form': form})

    def post(self, request, artist_id=None):

        form = AppointmentForm(request.POST)
        if form.is_valid():

            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.save()
            messages.success(request, "Appointment was requested "
                             "successfully! We will be in touch shortly.")
            return redirect('appointment')

        return render(request, 'appointment_form.html', {'form': form})

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please log in to create an appointment.')
        return super().dispatch(request, *args, **kwargs)


# Class for viewing appointments
class AppointmentView(LoginRequiredMixin, View):
    template_name = 'appointment.html'
    login_url = '/login/?next=/appointments/'
    context_object_name = 'appointments'

    def get(self, request):
        appointments = Appointment.objects.filter(user__email=request.user.email)
        return render(request, self.template_name,
                      {'appointments': appointments})

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please log in to view your appointments.')
        return super().dispatch(request, *args, **kwargs)


# Class for deleting appointments
class AppointmentDeleteView(LoginRequiredMixin, DeleteView):
    def post(self, request, appointment_id):
        appointment_to_delete = Appointment.objects.get(id=appointment_id)
        appointment_to_delete.delete()
        messages.success(request, "Appointment has been successfully deleted!")
        return redirect('appointment')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please log in to delete appointments.')
        return super().dispatch(request, *args, **kwargs)


# Function for editing appointments
# https://openclassrooms.com/en/courses/6967196-create-a-web-application-with-django/7349667-update-a-model-object-with-a-modelform
def appointment_update(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)

    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('appointment')
    else:
        form = AppointmentForm(instance=appointment)

    return render(request, 'edit_appointment.html', {'form': form})

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please log in to edit your appointments.')
        appointment = self.get_object()
        if self.request.user != appointment.user:
            messages.error(request, "You're trying to edit someone"
                           " else's appointment")
        return super().dispatch(request, *args, **kwargs)
