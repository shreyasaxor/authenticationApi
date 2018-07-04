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


# def post(self, request, *args, **kwargs):
#     data = {}
#     files = []
#     try:
#         for file in request.FILES.getlist('myfile'):
#             customer_obj = CustomerUser.objects.get(email=request.user.email)
#             domain_url = str(customer_obj.subdomain) + ".localhost"
#             try:
#                 obj = FaqKb.objects.get(issuecategory_id=request.POST['issue_id'])
#                 file_path = "media/" + domain_url + "/" + str(obj.file_path)
#                 if os.path.isfile(file_path):
#                     os.remove(file_path)
#             except:
#                 obj = FaqKb()
#             obj.issuecategory_id = request.POST['issue_id']
#             obj.file_name = file
#             obj.file_path = file
#             obj.tenant_id_id = request.user.tenant_id_id
#             obj.file_size = str(int(file.size) / 1024) + '/kb'
#             obj.save()
#             files.append(
#                 {'name': str(obj.file_name), 'path': str(domain_url) + '/' + str(obj.file_path), 'id': str(obj.id)})
#             data['files'] = files
#     except:
#         data.update(base_fail_message())
#     return HttpResponse(json.dumps(data), content_type='application/json')