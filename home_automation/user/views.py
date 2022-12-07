from rest_framework.views import APIView
from home_automation.user.models import MyUser
from home_automation.user.serializers import UserSerializer, UserLoginSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from home_automation.user.renderers import UserRenderer
from django.contrib.auth import authenticate
from django.http import Http404

# Generate Token Manually


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserList(APIView):
    """
    Retrieve all, post a user instance.
    """
    renderer_classes = [UserRenderer]

    def get(self, request):
        user_data = MyUser.objects.all()
        serializer = UserSerializer(user_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({'token': token, 'msg': 'Registration Successful'}, status=status.HTTP_201_CREATED)


class UserDetail(APIView):
    """
    Retrieve, update or delete a user instance.
    """
    renderer_classes = [UserRenderer]

    def get_object(self, pk):
        try:
            return MyUser.objects.get(pk=pk)
        except MyUser.DoesNotExist as e:
            raise Http404 from e

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserLoginView(APIView):
    """
    User login api with JWT token.
    """
    renderer_classes = [UserRenderer]
    
    def post(self, request, format=None):


        # from django.core.mail import EmailMultiAlternatives

        # subject, from_email, to = 'hello', 'pminesh470@gmail.com', 'mip.globaliasoft@gmail.com'
        # text_content = 'This is an important message.'
        # html_content = '<p>This is an <strong>important</strong> message.</p>'
        # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        # msg.attach_alternative(html_content, "text/html")
        # msg.send()



        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)
        if user is None:
            return Response({'errors': {'non_field_errors': ['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)
        token = get_tokens_for_user(user)
        return Response({'token': token, 'msg': 'Login Success'}, status=status.HTTP_200_OK)


# # user registration web socket api
# # ===============================================================================Start


# def UserRegistration(data):
#     try:
#         request_data = data
#         serializer = UserSerializer(data=request_data)
#         if not serializer.is_valid():
#             return "Invalid Data"
#         serializer.save()
#         return "User added successfully"
#     except Exception as e:
#         return "Something went wrong!"
# # ===============================================================================End

# # user listing web socket api
# # ===============================================================================Start


# def UserListing():
#     try:
#         all_user = UserModel.objects.all()
#         serializer = UserSerializer(all_user, many=True)
#         return serializer.data
#     except Exception as e:
#         return "Something went wrong!"
# # ===============================================================================End
