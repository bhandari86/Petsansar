import base64
import io
from io import BytesIO
from math import ceil
from django.contrib.auth.decorators import login_required

import matplotlib.pyplot as plt
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.db.models import Count
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import (DjangoUnicodeDecodeError, force_bytes,
                                   force_str)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import View
from matplotlib.figure import Figure
from django.db.models import Q 
from django.contrib.auth.decorators import login_required 
from petsansar.models import (AdoptionRequest, Animal, Contact, Donation,Strayanimalrescue,
                              RescueLocation, Strayanimal, Surrender, Notification,ListAdoptionRequest)

from .forms import AdoptionRequestForm
from .utils import TokenGenerator, generate_token


# Create your views here.
def index(request):
    allAnimal = []
    animals = Animal.objects.values('animaltype', 'id')
    animal = {item['animaltype'] for item in animals}
    for pet in animal:
        pets = Animal.objects.filter(animaltype=pet)
        n = len(pets)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allAnimal.append([pets, range(1, nSlides), nSlides])
    params = {'allAnimal': allAnimal}

    return render(request, "index.html", params)


def animaldetails(request, animal_id):
    animal = get_object_or_404(Animal, id=animal_id)
    return render(request, "animaldetails.html", {'animal': animal})


def adopt(request):
    allanimal = Animal.objects.all()
    return render(request, "adoption.html")


def donation(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            name = request.POST.get('name')
            pnumber = request.POST.get('pnumber')
            desc = request.POST.get('desc')
            myquery = Contact(name=name, desc=desc, phonenumber=pnumber)
            myquery.save()
            messages.info(request, "we will get back to you soon ....")
            return render(request, "contact.html")
        return render(request, "donation.html")
    else:
        messages.warning(request, 'You must be logged in to  give doanation.')
        return redirect('/login')
    return render(request, "donation.html")


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        desc = request.POST.get('desc')
        pnumber = request.POST.get('pnumber')
        myquery = Contact(name=name, email=email, desc=desc, phonenumber=pnumber)
        myquery.save()
        messages.info(request, "we will get back to you soon ....")
        return render(request, "contact.html")

    return render(request, "contact.html")


def list(request):
    pets = Surrender.objects.filter(is_approved=True)
    return render(request, "list.html", {'pets': pets})


def signup(request):
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        password=request.POST['pass1']
        confirm_password=request.POST['pass2']
        if password != confirm_password:
            messages.warning(request,"password is not matching ")
            return render(request,"signup.html")

        try:
            if User.objects.get(username=email):
                messages.warning(request,"Email is Taken")
                return render(request,'signup.html')
        except User.DoesNotExist:
            pass
        user = User.objects.create_user(username=email,email=email,password=password)
        user.is_active=False
        user.save()
        email_subject="Active your Account"
        message=render_to_string('activate.html',{
            'user':user,
            'domain':'127.0.0.1:8000',
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':generate_token.make_token(user)
            
            })
        email = EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email])
        email.send()
        messages.success(request,"activate your account by clicking the link in your gmail ")
        return redirect('/login')    
        return HttpResponse("User Created",email)
    return render(request,"signup.html")


def aboutus(request):
    return render(request, "aboutus.html")


class ActivateAccountView(View):
    def get(self,request,uidb64,token):
        try:
            uid=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
        except Exception as identifier:
            user=None
        if user is not None and generate_token.check_token(user,token):
            user.is_active=True 
            user.save()
            messages.info(request,"Account Activated successfully")
            return redirect('/login')
        return render(request,"activatefail.html")


def handlelogin(request):
    if request.method=="POST":
        username=request.POST.get('email')
        userpassword=request.POST.get('pass1')
        myuser=authenticate(request,username=username,password=userpassword)
        if myuser is not None:
            login(request, myuser)
            messages.success(request,"Login Success")
            return redirect('/')
        else:
            messages.error(request,"Invalid Credentials")
            return redirect('/login')
    return render(request,"login.html")


def dog(request):
    return render(request, "dog.html")


def approved_animal(request, id):
    animal = get_object_or_404(Surrender, ianimal_id=id)
    animal.is_approved = True
    animal.save()
    return render(request, "list.html", animal=animal)


def handlelogout(request):
    logout(request)
    messages.info(request, "logout success")
    return redirect('/login')


def blog(request):
    return render(request, "blog.html")


def search(request):
    if request.method =='GET':
        query = request.GET.get('query')
        
        if query:
            animals = Animal.objects.filter(animaltype__icontains=query)
            return render(request,"searchresult.html",{'animals':animals})
        else:
            print("No Information Shows")
            return render(request,"search.html")

# @login_required()
def surrender(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            pet = Surrender()
            pet.animaltype = request.POST.get('animaltype')
            pet.breeds = request.POST.get('breeds')
            pet.color = request.POST.get('color')
            pet.desc = request.POST.get('desc')
            pet.DOB = request.POST.get('dob')
            pet.sex = request.POST.get('sex')
            pet.weight = request.POST.get('weight')
            pet.medical_condition = request.POST.get('medical')
            pet.medicial_certificate = request.POST.get('mcertificate')
            pet.location = request.POST.get('location')

            if len(request.FILES) != 0:
                pet.image = request.FILES['image']
            pet.save()
            messages.success(request, "successfully surrendered")
            return redirect('/')
        return render(request, "surrender.html")
    else:
        messages.warning(request, 'You must be logged in to submit an surrender request.')
        return redirect('/login')
    return render(request, "surrender.html")



def verify_payment(request):
    data = request.POST

    animal_id = data['product_identity']
    token = data["token"]
    amount = data["amount"]
    print(product_ids)

    url = "https://khalti.com/api/v2/payment/verify/"
    payload = {"token": token, "amount": amount}
    headers = {
        "Authorization": "Key test_secret_key_7b5cd6f094dd496a92eb340bdf50ee96"}

    response = requests.request("POST", url, headers=headers, data=payload)

    response_data = json.loads(response.text)
    status_code = str(response.status_code)

    if status_code == "400":
        response = JsonResponse(
            {"status": "false", "message": response_data["detail"]}, status=500
        )
        return response

    import pprint

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(response_data)

    # After payment is verified, save the order in database
    # if response_data['idx']:
    #     for id in product_ids:
    #         order = OrderPlaced(user=request.user, )
    #         order.save()
    #     cart = Cart.objects.filter(user=request.user)
    #     cart.delete()

    return JsonResponse(
        f"Payment Done !! With IDX. {response_data['user']['idx']}", safe=False
    )


def rescue(request):
    return render(request, "rescue.html")


def adoption_map(request):
    animals = StrayAnimal.objects.all()
    return render(request, "adoption_map.html", {'animals': animals})


def rescue_map(request):
    rescue_locations = RescueLocation.objects.all()
    return render(request, "rescue_map.html", {'rescue_locations': rescue_locations})


def adoption_stats(request):
    adopted_count = Animal.objects.filter(adopted=True).count()
    not_adopted_count = Animal.objects.filter(adopted=False).count()

    fig = Figure()
    ax = fig.add_subplot(111)
    ax.pie([adopted_count, not_adopted_count], labels=["Adopted", "Not Adopted"], autopct='%1.1f%%')
    ax.set_title('Animal Adoption Statistics')

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    chart_data = base64.b64encode(buf.getvalue()).decode()

    context = {
        'adopted_count': adopted_count,
        'not_adopted_count': not_adopted_count,
        'chart_data': chart_data,
    }
    return render(request, "adoption_status.html", context)


def surrender_stats(request):
    surrender_count = Surrender.objects.filter(is_approved=True).count()
    not_surrender_count = Surrender.objects.filter(is_approved=False).count()

    fig = Figure()
    ax = fig.add_subplot(111)
    ax.pie([surrender_count, not_surrender_count], labels=["surrender", "Not surrender"], autopct='%1.1f%%')
    ax.set_title('Animal Surrender Statistics')

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    chart_data = base64.b64encode(buf.getvalue()).decode()

    context = {
        'surrender_count': surrender_count,
        'not_surrender_count': not_surrender_count,
        'chart_data': chart_data,
    }
    return render(request, "surrender_stats.html", context)

# @login_required()
def rescue_form(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pet = Strayanimalrescue()
            pet.name = request.POST.get('name')
            pet.phone = request.POST.get('Phone')
            pet.location = request.POST.get('location')
            pet.latitude = request.POST.get('latitude')
            pet.longitude = request.POST.get('longitude')
            pet.description = request.POST.get('description')
            # pet.DOB = request.POST.get('dob')
            # pet.sex = request.POST.get('sex')
            # pet.weight = request.POST.get('weight')
            # pet.medical_condition = request.POST.get('medical')
            # pet.location = request.POST.get('location')

            if len(request.FILES) != 0:
                pet.image = request.FILES['image']
            pet.save()
            messages.success(request, "successfully Requested")

        return render(request, "rescue_form.html")
    else:
            messages.warning(request, 'You must be logged in to submit an Rescue  request.')
            return redirect('/login')
            return render(request, "rescue_form.html")


def thankyou(request):
    return render(request, "thankyou.html")


def adoption_request(request, animal_id):
    animal = get_object_or_404(Animal, pk=animal_id)
    return render(request, "adoption_request.html", {'animal': animal})

def submit_adoption_request(request, animal_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            animal = Animal.objects.get(pk=animal_id)
            user = request.user
            contact = request.POST['contact']
            address = request.POST['address']
            description = request.POST['description']
            status = 'pending'

            AdoptionRequest.objects.create(
                animal=animal,
                user=user,
                contact=contact,
                address=address,
                description=description,
                status=status
            )

            animal.available_for_adoption = False
            animal.save()
            messages.success(request, 'Adoption request submitted successfully!')

            return redirect('/')

        else:
            animal = Animal.objects.get(pk=animal_id)
            user = request.user
            context = {
                'animal': animal,
                'user': user,
            }
    else:
        messages.warning(request, 'You must be logged in to submit an adoption request.')
        return redirect('/login')
    return render(request, 'adoption_request.html', context)

def view_notifications(request):
    user_notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'notifications': user_notifications
    }
    return render(request, 'notifications.html', context)
def list_request(request, animal_id):
    pet = get_object_or_404(Surrender, pk=animal_id)
    return render(request, "list_request.html", {'pet': pet})    

def submit_list_adoption_request(request, animal_id):
    pet = get_object_or_404(Surrender, pk=animal_id)    
    return redirect('/')


def submit_list_adoption_request(request, animal_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pet = Surrender.objects.get(pk=animal_id)
            user = request.user
            contact = request.POST['contact']
            address = request.POST['address']
            description = request.POST['description']
            status = 'pending'

            list_request = ListAdoptionRequest.objects.create(
                pet=pet,
                user=user,
                contact=contact,
                address=address,
                description=description,
                status=status
            )
            pet.available_for_adoption = False
            pet.save()
            messages.success(request, 'Adoption request submitted successfully!')

            return redirect('/') 

        else:
            pet = Surrender.objects.get(pk=animal_id)
            user = request.user
            context = {
                'pet': pet,
                'user': user,
            }
    else:
        messages.warning(request, 'You must be logged in to submit an adoption request.')
        return redirect('/login')
        return render(request, 'adoption_request.html', context)