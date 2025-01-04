from functools import wraps
from rest_framework_simplejwt.tokens import AccessToken
from django.http import JsonResponse
from django.contrib.auth.models import User

def jwt_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        token = request.COOKIES.get('access_token')
        if not token:
            return JsonResponse({'error': 'Токен отсутствует'}, status=401)

        try:
            access_token = AccessToken(token)
            user_id = access_token.get('user_id')
            if not user_id:
                return JsonResponse({'error': 'Не удалось найти пользователя'}, status=401)
            user = User.objects.get(id=user_id)
            if not user:
                return JsonResponse({'error': 'Пользователь не найден'}, status=401)

            request.user = user
        except Exception as e:
            print(f'Ошибка: {e}')
            return JsonResponse({'error': 'Неверный токен'}, status=401)

        return view_func(request, *args, **kwargs)

    return _wrapped_view