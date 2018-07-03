# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializer import UserSerializers
from .utils import generate_secretkey,authenticate_key
from rest_framework.authtoken.models import Token
# Create your views here.


class GetUser(APIView):

    def get(self,request):
        data ={}
        obj=User.objects.all()
        serializer = UserSerializers(obj ,many=True)
        return Response(serializer.data)


    def post(self,request,*args,**kwargs):
        data={}
        try:
            serializer=UserSerializers(data=request.data)
            if serializer.is_valid():
                id  = serializer.save()
                secret_key = generate_secretkey(request.data['email'])
                token = Token.objects.get_or_create(user=id)
                data['status']=1
                data['secret_key']=secret_key
                data['token']=token.key
                return Response(data, status=status.HTTP_200_OK)
            else:
                data['status'] = 0
                return Response({'data':serializer.errors}, status=status.HTTP_200_OK)
        except:
            raise
get_user = GetUser.as_view()
