from rest_framework import permissions
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from student.models import Student, Marks
from student.serializers import StudentSerializer, MarksSerializer
from teacher.api_views import TeacherView, TeachesView

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


class SearchView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):

        if request.POST.get('search_whom') == 'Student':

            """
                This condition returns the serialized data of Student if exist else returns error response 
            """

            try:
                student_serializer = StudentView.get(self, request, pk=request.POST.get('id'))

                student_serializer['student_image'] = SERVER_DOMAIN + student_serializer['student_image']

                return Response({'result': student_serializer}, status=status.HTTP_200_OK)
            except Exception:
                return Response({'Error': 'Wrong search credentials'}, status=status.HTTP_400_BAD_REQUEST)
        elif request.POST.get('search_whom') == 'Teacher':

            """
                This condition returns the serialized data of Teacher if exist else returns error response 
            """

            try:
                teacher_serializer_data = TeacherView.get(self, request, pk=request.POST.get('id'))
                teaches_serialized_data = TeachesView.get(self, request, pk=request.POST.get('id'))

                teacher_serializer_data['teacher_image'] = SERVER_DOMAIN + teacher_serializer_data['teacher_image']
                teacher_serializer_data['teaches'] = teaches_serialized_data

                return Response({'result': teacher_serializer_data}, status=status.HTTP_200_OK)
            except Exception:
                return Response({'Error': 'Wrong search credentials'}, status=status.HTTP_400_BAD_REQUEST)

        else:

            """
                This condition returns error response
            """

            return Response({'Error': 'Wrong search credentials'}, status=status.HTTP_400_BAD_REQUEST)
