from rest_framework import permissions
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from student.models import Student, Marks
from student.serializers import StudentSerializer, MarksSerializer

SERVER_DOMAIN = 'http://127.0.0.1:8000'


class StudentView(APIView):

    def get(self, request, *args, **kwargs):
        return StudentSerializer(instance=Student.objects.get(admission_number=kwargs['pk'])).data


class MarksView(APIView):

    def get(self, request, *args, **kwargs):
        return MarksSerializer(many=True, instance=Marks.objects.filter(admission_number=kwargs['pk'])).data


class DashboardView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        pk = self.get_pk(request)
        student_serializer = StudentView.get(self, request, pk=pk)
        marks_serializer = MarksView.get(self, request, pk=pk)

        student_serializer['subjects'] = marks_serializer

        student_serializer['student_image'] = SERVER_DOMAIN + student_serializer['student_image']
        return Response({'student': student_serializer}, status=status.HTTP_200_OK)

    def get_pk(self, request):
        token = request.headers['authorization'].split(' ')[1]
        return Token.objects.get(key=token).user.username