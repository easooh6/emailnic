from django.shortcuts import render
from .models import User
import json
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import EmptyResultSet
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt

def create_user(request):
    if request.method == "POST":
        data =  json.loads(request.body)
        mail = data['mail']
        firstname = data['firstname']
        lastname = data['lastname']
        user = User.objects.create(mail=mail,firstname=firstname,lastname=lastname)
        
        return JsonResponse({'id': user.id}, status=201)

def get_users(request):
    people = User.objects.all()
    data_people = []    
    for person in people:
        data_people.append({
            'id' : person.id,
            'mail' : person.mail,
            'firstname' : person.firstname,
            'lastname' : person.lastname
        })
    return JsonResponse({'users': data_people})

def get_user(request):
    try:    
        user = json.loads(request.body)
        user_id = user.get("id")
    except json.JSONDecodeError:
        return JsonResponse({"error": "invalid id"}, status=400)
    try:
        person = User.objects.get(id = user_id)
    except User.DoesNotExist:
        return JsonResponse({'user': "no such user"})
    
    data = {
        'id' : person.id,
        'mail': person.mail,
        'firstname' : person.firstname,
        'lastname' : person.lastname
        }
    return JsonResponse({'user': data})

@csrf_exempt
def delete_user(request):
    try:
        person_id = request.GET['id']
    except KeyError:
        return JsonResponse({'id': "invalid id"})
    try:
        person = User.objects.get(id = person_id)
    except User.DoesNotExist:
        return JsonResponse({'id': "no such user"})
    person.delete()
    return JsonResponse({"id":"was deleted"},status=204)
@csrf_exempt
def update_user(request):
    if request.method == "PATCH":
        try:
            data = json.loads(request.body)
            person = User.objects.get(id=data['id'])
            if 'mail' in data:
                person.mail = data['mail']
            if 'firstname' in data:
                person.firstname = data['firstname']
            if 'lastname' in data:
                person.lastname = data['lastname']
            person.save()
            return JsonResponse({'id':person.id,
                                 'mail':person.mail,
                                 'firstname':person.firstname,
                                 'lastname':person.lastname
                                 },status=200)
        except User.DoesNotExist:
            return JsonResponse({'id': "no such user"})
        
@csrf_exempt
def send_to_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        users = data.get('id', [])
        message = data.get('message','')
        if len(users) == 0 or len(message) == 0:
            return JsonResponse({"error":"the message is empty or user is not found"})
        for person in users:
            user = User.objects.get(id=person)
            send_mail(
                subject = "a new mail",
                message = '',
                from_email = settings.EMAIL_HOST_USER,
                recipient_list= [user.mail],
                html_message= message,
                fail_silently=False)
        return JsonResponse({"success":"the mail was sent"})



    
