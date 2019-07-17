import hmac

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.cache import cache
from django.core.exceptions import PermissionDenied


class IsAuthenticated(object):
    @staticmethod
    def has_permission(permission):
        def real_decorator(function):
            def function_wrapper(self, request, *args, **kwargs):
                try:
                    x_key = request.META['HTTP_X_KEY']
                    x_route = request.META['HTTP_X_ROUTE']
                    x_signature = request.META['HTTP_X_SIGNATURE']

                    x_route = x_route.split(';')
                    x_route.sort()
                    x_route = ';'.join(x_route)
                    x_route = str.encode(x_route)

                    signature = hmac.new(x_route, str.encode(x_key))
                    if x_signature == signature.hexdigest():
                        return function(self, request, *args, **kwargs)
                    raise PermissionDenied()
                except Exception as e:
                    print(str(e))
                    raise PermissionDenied()
                raise PermissionDenied()
            return function_wrapper
        return real_decorator


class CredentialView(APIView):
    def put(self, request):
        try:
            key = request.data['key']
            shared_secret = request.data['shared_secret']

            if cache.get(key):
                return Response(status=status.HTTP_403_FORBIDDEN)

            cache.set(key, shared_secret)
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            data = 'Error en la petición, falta el objeto {}' \
                .format(str(e))
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


class MessagesListView(APIView):
    @IsAuthenticated.has_permission(None)
    def post(self, request):
        try:
            msg = request.data['msg']
            tags = request.data['tags']

            message_id = cache.get('message_id')
            if not message_id:
                message_id = 1
            else:
                cache.set('message_id', message_id + 1)

            data = {
                'id': message_id,
                'msg': msg,
                'tags': tags
            }

            cache.set(message_id, data)
            return Response(data=data, status=status.HTTP_200_OK)
        except Exception as e:
            data = 'Error en la petición, falta el objeto {}' \
                .format(str(e))
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


class MessagesDetailView(APIView):
    @IsAuthenticated.has_permission(None)
    def get(self, request, id):
        data = cache.get(id)
        if data:
            return Response(data=data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class MessagesDetailTagView(APIView):
    def get(self, request, tag):
        print(tag)
        return Response(status=status.HTTP_200_OK)
