from rest_framework import serializers

from teacher.models import Teacher, Teaches


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = "__all__"


class TeachesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teaches
        fields = "__all__"
