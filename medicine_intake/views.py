from django.http import HttpResponse
from rest_framework.generics import CreateAPIView
from medicine_intake.models import RegisterUser,Task_medicine
from rest_framework import generics, status
from medicine_intake.serializers import UserRegisterSerializer,GelUserDetailsSerializer,Task_medicineSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils import timezone  
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view



def index(request):
    return HttpResponse("Hello, world.")


class CreateUserRegister(CreateAPIView):
    model = RegisterUser
    permission_classes = (AllowAny,)
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            #return Response([serializer.data], status=status.HTTP_200_OK)
            return Response({
                "CreateUser": serializer.data,
                "message": "register successfully!",
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)

        # print(serializer.errors)
        try:
            return Response({'Error': serializer.errors['email'][0]}, status=status.HTTP_400_BAD_REQUEST)
        except:
            pass

        try:
            return Response({'Error': serializer.errors['password2'][0]}, status=status.HTTP_400_BAD_REQUEST)
        except:
            pass

        try:
            return Response({'Error': serializer.errors['mob_no'][0]}, status=status.HTTP_400_BAD_REQUEST)
        except:
            pass

        return Response({'Error': "Something Went Wrong !"}, status=status.HTTP_400_BAD_REQUEST)


class AppToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})

        if serializer.is_valid():
            user = serializer.validated_data['user']
            password = serializer.validated_data['password']

            token, created = Token.objects.get_or_create(user=user)

            registerUser = RegisterUser.objects.filter(userId=token.user.id, email=token.user).values('userId','id',
                                                                                                      'email',
                                                                                                      'first_name',
                                                                                                      'last_name',
                                                                                                      'mob_no')
            # print(registerUser[0])
            context = {"token": token.key, "userId": registerUser[0]['userId'], "email": registerUser[0]['email'],
                       "first_name": registerUser[0]['first_name'], "last_name": registerUser[0]['last_name'],
                       "mob_no": registerUser[0]['mob_no'], "id": registerUser[0]['id'],
                       }

            #return Response([context], status=status.HTTP_200_OK)
            return Response({
                "Login": context,
                "message": "Login successfully!",
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)

        try:
            return Response({'Error': serializer.errors['non_field_errors'][0]}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'Error': "Please Provide Username and Password"}, status=status.HTTP_400_BAD_REQUEST)
        # return JsonResponse({'message':'ok'}, status=status.HTTP_400_BAD_REQUEST)

class GetUserProfileDetails(APIView):
    # parser_classes = (MultiPartParser, FormParser, FileUploadParser)
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            pk = pk
            return RegisterUser.objects.get(pk=pk)
        except RegisterUser.DoesNotExist:
            raise Http404

    def get(self, request, pk=None):
        data = RegisterUser.objects.filter(userId=request.user.id)
        serializer = GelUserDetailsSerializer(data, many=True)
        if data:
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"something went wrong!"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        id = pk
        instance = self.get_object(id)

        serializer = GelUserDetailsSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response({
                "Userprofile": serializer.data,
                "message": "updated successfully!",
                "status": status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)      


class MedicineList(APIView):
    permission_classes = (IsAuthenticated,)
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):

        snippets = Task_medicine.objects.all()
        serializer = Task_medicineSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = Task_medicineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class MedicineDetail(APIView):
    permission_classes = (IsAuthenticated,)
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Task_medicine.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = Task_medicineSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = Task_medicineSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)






