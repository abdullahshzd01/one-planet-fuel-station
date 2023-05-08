from django.db.models import Q
from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from APIs.Serializers.ApplicationSerializer import JobApplicationSerializer
from APIs.Serializers.JobSerializer import JobsSerializer
from app.models import *


class JobsList(generics.ListAPIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = jobs.objects.all()
    serializer_class = JobsSerializer

    def get_queryset(self):
        queryset = jobs.objects.all()
        title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(Q(job_name__icontains=title))
        stationID = self.request.query_params.get('stationID', None)
        if stationID is not None:
            queryset = queryset.filter(Q(fuelStation__id=stationID))
        return queryset


class JobDetail(generics.RetrieveAPIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = jobs.objects.all()
    serializer_class = JobsSerializer

    def get_object(self):
        id = self.kwargs.get('pk')
        return jobs.objects.get(pk=id)


class ApplicationCreate(generics.CreateAPIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = applicant.objects.all()
    serializer_class = JobApplicationSerializer


    def create(self, request, *args, **kwargs):
        email = request.data['email']
        user = None
        if users.objects.filter(email=email).exists():
            user = users.objects.get(email=email)
        else:
            user = users()
            user.email = email
            user.firstName = email.split('@')[0]
            user.lastName = email.split('@')[0]
            user.phone = email.split('@')[0]
            user.save()

        print(request.data)
        files = request.FILES
        newApplication = applicant()
        newApplication.user = user
        newApplication.job = jobs.objects.get(pk=request.data['job'])
        if 'cv' in files:
            newApplication.cv = files['cv']
        newApplication.save()
        return Response(status=status.HTTP_201_CREATED)



    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        print(instance)
        serializer = -JobApplicationSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)