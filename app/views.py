import os
import uuid
from django.http import FileResponse, JsonResponse
from django.shortcuts import render
from .models import Docs, Ratings, Users


def about(request):
    """Функция представления показывает страницу с информацией о сайте."""

    return render(request, 'app/about.html')


def delete_file(request):
    """Функция представления обрабатывает запрос на удаление файла."""

    if request.method == 'POST':
        # Получаем имя пользователя, токен доступа, Id файла, который нужно
        # удалить
        name = request.POST.get('username')
        token = request.POST.get('token')
        file_id = request.POST.get('file_id')
        if not name or not token or not file_id:
            return JsonResponse(
                {'text': 'Не указано имя, код доступа или Id файла'}, status=400)
        # Имя, код доступа и Id файла непустые
        try:
            user = Users.objects.get(name=name, token=token)
        except Users.DoesNotExist:
            return JsonResponse({'text': 'Неверное имя или код доступа'},
                                status=400)
        # Пользователь найден, код доступа верен. Получаем документ по Id
        doc = user.docs_set.filter(id=file_id)
        if doc:
            # Файл найден. Удаляем его
            print(dir(doc))
            doc.delete()
            return JsonResponse({}, status=200)
        # Файла нет
        return JsonResponse({'text': 'Файл не найден'}, status=400)


def download_file(request):
    """Функция представления обрабатывает запрос на скачивание файла."""

    if request.method == 'GET':
        # Получаем Id файла, который нужно скачать
        file_id = request.GET.get('file_id')
        try:
            doc = Docs.objects.get(id=file_id, access=True)
        except Docs.DoesNotExist:
            return JsonResponse({'text': 'Файл не найден'}, status=400)
        # Файл найден и он доступен. Считываем файл и отправляем
        return FileResponse(open(doc.filepath, 'rb'))
    return JsonResponse({'text': 'Неизвестный запрос'}, status=400)


def estimate_file(request):
    """Функция представления обрабатывает запрос на оценку документа."""

    if request.method == 'GET':
        # Получаем Id файла и изменение рейтинга
        file_id = request.GET.get('file_id')
        rating = int(request.GET.get('rating'))
        try:
            doc = Docs.objects.get(id=file_id, access=True)
        except Docs.DoesNotExist:
            return JsonResponse({'text': 'Файл не найден'}, status=400)
        # Файл найден и он доступен
        doc.rating += rating
        doc.save()
        return JsonResponse({'rating': doc.rating}, status=200)
    return JsonResponse({'text': 'Неизвестный запрос'}, status=400)


def exit(request):
    """Функция представления для выхода из личного кабинета."""

    # Получаем имя пользователя и код доступа
    name = request.GET.get('username')
    token = request.GET.get('token')
    if not name and not token:
        return JsonResponse({'text': 'Не указано имя или код доступа'},
                            status=400)
    # Имя и код доступа непустые
    try:
        user = Users.objects.get(name=name, token=token)
    except Users.DoesNotExist:
        return JsonResponse({'text': 'Неверное имя или код доступа'},
                            status=400)
    # Удаляем код доступа
    user.token = None
    user.save()
    return JsonResponse({'username': name}, status=200)


def index(request):
    """Функция представления показывает главную страницу."""

    # Получаем данные о доступных всем пользователям документах
    available_docs = Docs.objects.filter(access=True)
    docs = []
    for doc in available_docs:
        description = doc.description if doc.description else ''
        doc_info =\
            {'file_id': doc.id, 'name': os.path.basename(doc.filepath),
             'description': description,
             'date': doc.date.strftime('%d.%m.%Y %H:%M'),
             'size': doc.size, 'rating': doc.rating}
        docs.append(doc_info)
    return render(request, 'app/index.html', context={'docs': docs})


def private(request):
    """Функция представления показывает страницу с личным кабинетом."""

    # Имя пользователя и код доступа
    name = request.GET.get('username')
    token = request.GET.get('token')
    # Ищем пользователя по имени и коду доступа
    try:
        user = Users.objects.get(name=name, token=token)
    except Users.DoesNotExist:
        # Пользователь не зарегистрирован или неверный код доступа
        return render(request, 'app/index.html')
    # Получаем данные о документах пользователя
    user_docs = Docs.objects.filter(user__name=name)
    docs = []
    for doc in user_docs:
        description = doc.description if doc.description else ''
        doc_info =\
            {'file_id': doc.id, 'name': os.path.basename(doc.filepath),
             'description': description,
             'date': doc.date.strftime('%d.%m.%Y %H:%M'),
             'size': doc.size, 'rating': doc.rating, 'access': doc.access}
        docs.append(doc_info)
    return render(request, 'app/private.html',
                  context={'username': name, 'docs': docs})


def private_start(request):
    """Функция представления для определения авторизован ли пользователь."""

    return render(request, 'app/private_start.html')


def save_file(request):
    """Функция представления сохраняет изменения в описании и доступе к
    документу."""

    if request.method == 'POST':
        # Получаем имя, код доступа, Id, описание и доступ к документу
        name = request.POST.get('username')
        token = request.POST.get('token')
        file_id = request.POST.get('file_id')
        description = request.POST.get('description')
        access = request.POST.get('access')
        if not name or not token or not file_id:
            return JsonResponse(
                {'text': 'Не указано имя, код доступа или Id файла'}, 400)
        # Имя, код доступа и Id файла непустые
        try:
            user = Users.objects.get(name=name, token=token)
        except Users.DoesNotExist:
            return JsonResponse({'text': 'Неверное имя или код доступа'},
                                status=400)
        # Пользователь найден, код доступа верен. Получаем документ по Id
        doc = user.docs_set.filter(id=file_id)
        if doc:
            access = True if access == 'true' else False
            doc.update(description=description, access=access)
            return JsonResponse({}, status=200)
        return JsonResponse({'text': 'Файл не найден'}, status=400)


def sign_in(request):
    """Функция представления показывает страницу с авторизацией."""

    if request.method == 'GET':
        return render(request, 'app/sign_in.html')
    if request.method == 'POST':
        # Получаем имя, пароль и параметр, отвечающий за вход или регистрацию
        name = request.POST.get('username')
        password = request.POST.get('password')
        is_sign_in = int(request.POST.get('sign_in'))
        if not name or not password:
            return JsonResponse({'text': 'Не указано имя или пароль'},
                                status=400)
        if is_sign_in:
            # Пользователь уже зарегистрирован, хочет войти в личный кабинет
            try:
                user = Users.objects.get(name=name)
            except Users.DoesNotExist:
                # Пользователь не зарегистрирован
                return JsonResponse({'text': 'Пользователь не зарегистрирован'},
                                    status=404)
            # Пользователь зарегистрирован
            if password == user.password:
                # Введен верный пароль. Генерируем случайный код доступа и
                # сохраняем
                uuid4 = uuid.uuid4()
                user.token = uuid4
                user.save()
                return JsonResponse({'username': name, 'token': uuid4},
                                    status=200)
            # Пароль неверный
            return JsonResponse({'text': 'Неверный пароль'}, status=401)
        else:
            # Пользователь регистрируется
            try:
                user = Users.objects.get(name=name)
            except Users.DoesNotExist:
                # Пользователь не зарегистрирован, регистрируем его, генерируем
                # случайный код доступа и сохраняем
                uuid4 = uuid.uuid4()
                user = Users.objects.create(name=name, password=password,
                                            token=uuid4)
                user.save()
                return JsonResponse({'username': name, 'token': uuid4},
                                    status=200)
            # Пользователь уже зарегистрирован
            return JsonResponse(
                {'text': 'Пользователь с указанным именем уже зарегистрирован'}, status=400)


def upload_file(request):
    """Функция представления обрабатывает запрос на загрузку файла на
    сервер."""

    if request.method == 'POST':
        # Получаем имя пользователя, токен доступа, файл и описание файла
        name = request.POST.get('username')
        token = request.POST.get('token')
        description = request.POST.get('description')
        file = request.FILES.get('file')
        if not name or not token or not file:
            return JsonResponse(
                {'text': 'Не указано имя, код доступа или файл'}, status=400)
        # Имя, код доступа и файл непустые
        try:
            user = Users.objects.get(name=name, token=token)
        except Users.DoesNotExist:
            return JsonResponse({'text': 'Неверное имя или код доступа'},
                                status=400)
        # Сохраняем файл на сервер
        filepath = f'db/{file.name}'  # путь, где сохранится файл на сервере
        with open(filepath, 'wb') as f:
            f.write(file.read())
        # Добавляем запись в базу данных
        doc = Docs(description=description, filepath=filepath, size=file.size)
        description = description if description else ''
        user.docs_set.add(doc, bulk=False)
        doc_info =\
            {'file_id': doc.id, 'name': os.path.basename(doc.filepath),
             'description': description,
             'date': doc.date.strftime('%d.%m.%Y %H:%M'),
             'size': doc.size, 'rating': doc.rating, 'access': doc.access}
        return JsonResponse(doc_info, status=200)
    return JsonResponse({'text': 'Неизвестный запрос'}, status=400)
