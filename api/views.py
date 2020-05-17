from django.shortcuts import render
from rest_framework import viewsets, status
from .models import Movie, Rating
from django.http import HttpResponse
from .serializers import MovieSerializer, RatingSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated



def trainModel(request):
    res = "Messasda"
    return HttpResponse(res)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes= (IsAuthenticated,)

    @action(detail= True, methods= ["POST"])
    def rate_movie(self, request,pk = None):
        
        movie = Movie.objects.get(id=pk)
        # user = User.objects.get(id=1)
        user = request.user
        print("USERIS", user)
        stars = request.data['stars']

        try:
            rating = Rating.objects.get(movie = movie.id, user= user.id)
            rating.stars = stars
            rating.save()
            serializer = RatingSerializer(rating, many= False)
            response = {'message': 'its working Updated', 'result': serializer.data}
            return Response(response, status= status.HTTP_200_OK)
        except:
            rating = Rating.objects.create(user = user, movie= movie, stars = stars)
            serializer = RatingSerializer(rating, many= False)
            response = {'message': 'its working Created', 'result': serializer.data}
            return Response(response, status= status.HTTP_200_OK)
        
       

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


