from django.shortcuts import redirect

class BlockCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.user.is_blocked:
            request.session.flush()  
            return redirect('user_login') 

        response = self.get_response(request)
        return response
