from django.shortcuts import render
from django.views.generic import View

# Create your views here.
class Index(View):

    def get(self,request):
        return render(request,"user/index.html")

    def post(self,request):
        pass