from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView


class ProfileView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = "accounts/profile_detail.html"

    def get_object(self):
        return self.request.user

