from rest_framework.views import APIView

from teacher.models import Teacher, Teaches
from teacher.serializers import TeacherSerializer, TeachesSerializer


class TeacherView(APIView):

    def get(self, request, *args, **kwargs):
        return TeacherSerializer(instance=Teacher.objects.get(teacher_id=kwargs['pk'])).data


class TeachesView(APIView):

    def get(self, request, *args, **kwargs):
        return TeachesSerializer(many=True, instance=Teaches.objects.filter(teacher_id=kwargs['pk'])).data
