from rest_framework import views, response


class UsersViews(views.APIView):
    def get(self, request):
        return response.Response({"message": "Hello, world!"})
