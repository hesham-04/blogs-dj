from django.shortcuts import HttpResponse, render



class UnderConstructionMiddleware():
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print('Call from Middleware before the view') #called before the view
        #response = self.get_response(request) #This is how the actual view is generated, now if we want the middle ware to interrup and show/do something else we will change the reponse variable
        response = render(request, 'main/underconstruction.html')
        print('Call from Middleware after the View')
        return response