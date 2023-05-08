from rest_framework import serializers
from app.models import *


class JobApplicationSerializer(serializers.ModelSerializer):
    # use this serializer to create a new job application
    job = serializers.PrimaryKeyRelatedField(read_only=False, required=True, allow_null=False,
                                             queryset=jobs.objects.all())
    # user will be an object . Check if user.email exists in the database if not create a new user
    user = serializers.PrimaryKeyRelatedField(read_only=False, required=True, allow_null=False,
                                                queryset=users.objects.all())
    cv = serializers.ImageField(read_only=False, required=False, allow_null=False)

    class Meta:
        model = applicant
        fields = "__all__"
        extra_kwargs = {
            "cv": {"required": False, "allow_null": True},
        }
