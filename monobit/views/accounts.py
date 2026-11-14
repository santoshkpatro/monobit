from django.views import View
from django.shortcuts import render


class AccountsLoginView(View):
    def get(self, request, **kwargs):
        return render(request, "accounts/login.html")

    def post(self, request, **kwargs):
        pass