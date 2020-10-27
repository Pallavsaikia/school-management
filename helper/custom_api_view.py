from rest_framework.views import APIView
from helper.check_token import check_token
from django.utils.decorators import method_decorator


@method_decorator(check_token, name='dispatch')
class AuthenticatedApiView(APIView):
    pass
