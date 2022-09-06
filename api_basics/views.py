from http.client import BAD_REQUEST
import imp
from telnetlib import STATUS
from django.shortcuts import render

from django.http.response import HttpResponse,JsonResponse 
from rest_framework.parsers import JSONParser

from api_basics.utilities.make_request import make_request
from .models import Article
from .serilizers import ArticleSerializer, CountrySerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins


class GenericArticleView(generics.GenericAPIView,mixins.DestroyModelMixin,mixins.ListModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin,mixins.RetrieveModelMixin):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    lookup_field = 'id'

    def get(self, request,id = None):
        if id:
            return self.retrieve(id)
        else:
            return self.list(request)

    def post(self, request):
        return self.create(request)

    def put(self, request,id = None):
        return self.create(request,id)

    def delete(self, request,id = None):
        return self.destroy(request,id)


class ArticleAPIView(APIView):
    def get(self, request):
        articles=Article.objects.all()
        serilizer=ArticleSerializer(articles,many=True)
        return Response(serilizer.data)
    
    def post(self, request):
        serilizer=ArticleSerializer(data=request.data)

        if serilizer.is_valid():
            serilizer.save()
            return Response(serilizer.data ,status=status.HTTP_201_CREATED)
        return Response(serilizer.errors,status=status.HTTP_400_BAD_REQUEST)



class ArticleDetailsAPIView(APIView):
    def get_object(self, id):
        try:
            return Article.objects.get(id=id)
        except Article.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def get(self, request, id):
        article = self.get_object(id)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    
    def put(self, request, id):
        article = self.get_object(id)
        serilizer=ArticleSerializer(article,data=request.data)
        if serilizer.is_valid():
            serilizer.save()
            return Response(serilizer.data )
        return Response(serilizer.errors,status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request, id):
        article = self.get_object(id)
        article.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)



# Create your views here.
@api_view(['GET','POST'])
@csrf_exempt
def article_list(request):
    if request.method=="GET":
        articles=Article.objects.all()
        serilizer=ArticleSerializer(articles,many=True)
        return Response(serilizer.data)

    elif request.method=="POST":
        serilizer=ArticleSerializer(data=request.data)

        if serilizer.is_valid():
            serilizer.save()
            return Response(serilizer.data ,status=status.HTTP_201_CREATED)
        return Response(serilizer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@csrf_exempt
def countries_list(request):
    if request.method=="GET":
        data_response = make_request('get','/v1/data/countries','')
        print(data_response)
        serizalizer = CountrySerializer(data_response)
        print("""
        serializer iss 

        """)
        print(serizalizer)
        # if serizalizer.is_valid():
        return Response(serizalizer.data)
        # else:
        #     return Response(serizalizer.errors,status=BAD_REQUEST)
        



@api_view(['GET','PUT','DELETE'])
@csrf_exempt
def article_detail(request, pk) :
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serilizer=ArticleSerializer(article,data=request.data)
        if serilizer.is_valid():
            serilizer.save()
            return Response(serilizer.data )
        return Response(serilizer.errors,status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        article.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

