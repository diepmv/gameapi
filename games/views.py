from django.shortcuts import render


# Create your views here.

from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.response import Response

from games.models import Game, GameCategory, Player, PlayerScore
from games.serializers import GameSerializer, GameCategorySerializer, PlayerSerializer, PLayerScoreSerializer
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse

from django.contrib.auth.models import User
from games.serializers import UserSerializer
from rest_framework import permissions
from games.permissions import IsOwnerOrReadOnly


# class JSONResponse(HttpResponse):
#     def __init__(self, data, **kwargs):
#         content = JSONRenderer().render(data)
#         kwargs['content_type'] = 'application/json'
#         super(JSONResponse, self).__init__(content, **kwargs)


#API function based views

# # @csrf_exempt
# @api_view(['GET', 'POST'])
# def game_list(request, format=None):
#     if request.method=='GET':
#         games = Game.objects.all()
#         games_serializer = GameSerializer(games, many=True)
#
#         # return JSONResponse(games_serializer.data)
#         return Response(games_serializer.data)
#
#
#     elif request.method =='POST':
#         game_data = JSONParser().parse(request)
#         game_serializer = GameSerializer(data=game_data)
#         if game_serializer.is_valid():
#             game_serializer.save()
#
#             # return JSONResponse(game_serializer.data, status=status.HTTP_201_CREATED)
#             return Response(game_serializer.data, status = status.HTTP_201_CREATED)
#
#     #
#     # return JSONResponse(game_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
#         return Response(game_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
#
#
#
#
# # @csrf_exempt
# @api_view(['GET', 'POST', 'DELETE'])
# def game_detail(request, pk, format=None):
#     try:
#         game = Game.objects.get(pk=pk)
#     except Game.DoesNotExist:
#         return HttpResponse(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         game_serializer = GameSerializer(game)
#         # return JSONResponse(game_serializer.data)
#         return Response(game_serializer.data)
#
#
#     elif request.method == 'PUT':
#         game_data = JSONParser().parse(request)
#         game_serializer = GameSerializer(game, data=game_data)
#         if game_serializer.is_valid():
#             game_serializer.save()
#             # return JSONResponse(game_serializer.data)
#             return Response(game_serializer.data)
# #         return JSONResponse(game_serializer.errors,
# # status=status.HTTP_400_BAD_REQUEST)
#         return Response(game_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         game.delete()
#         return HttpResponse(status=status.HTTP_204_NO_CONTENT)
#
#
#


#rewrite API using class_based views

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-list'

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-detail'

class GameList(APIView):
    def get(self, request, format=None):
        games = Game.objects.all()
        games_serializer = GameSerializer(games, many=True)
        return Response(games_serializer.data)

    def post(self, request, format=None):
        game_serializer = GameSerializer(request.data)
        if game_serializer.is_valid():
            game_serializer.save()
            return Response(game_serializer.data, status = status.HTTP_201_CREATED)
        return Response(game_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GameDetail(APIView):
    def get_object(self, pk):
        try:
            return Game.objects.get(pk=pk)
        except Game.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        game = self.get_object(pk)
        game_serialzier = GameSerializer(game)
        return Response(game_serialzier.data)

    def put(self, request, pk, format=None):
        game = self.get_object(pk)
        game_serializer = GameSerializer(game, data=request.data)
        if game_serializer.is_valid():
            game_serializer.save()
            return Response(game_serializer.data)
        return Response(game_serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        game = self.get_object(pk)
        game.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)


class GameCategoryList(generics.ListCreateAPIView):
    queryset = GameCategory.objects.all()
    serializer_class = GameCategorySerializer
    name = 'gamecategory-list'

class GameCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = GameCategory.objects.all()
    serializer_class = GameCategorySerializer
    name = 'gamecategory-detail'

class GameList(generics.ListCreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    name = 'game-list'

    def perform_create(self, serializer):
        #pass an additional owner field to the create method
        # To Set the owner to the user received in the request
        serializer.save(owner=self.request.user)

    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )




class GameDetail(generics.RetrieveDestroyAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    name = 'game-detail'

    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    )

class PlayerList(generics.ListCreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    name = 'player-list'

class PlayerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    name = 'player-detail'

class PlayerScoreList(generics.ListCreateAPIView):
    queryset = PlayerScore.objects.all()
    serializer_class = PLayerScoreSerializer
    name = 'playerscore-list'

class PlayerScoreDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PlayerScore.objects.all()
    serializer_class = PLayerScoreSerializer
    name = 'playerscore-detail'


class ApiRoot(generics.GenericAPIView):
    name = 'api-root'
    def get(self, request, *args, **kwargs):
        return Response({
            'player': reverse(PlayerList.name, request=request),
            'game-categories': reverse(GameCategoryList.name, request=request),
            'games': reverse(GameList.name, request=request),
            'scores': reverse(PlayerScoreList.name, request=request),
            'users': reverse(UserList.name, request=request),
        })

