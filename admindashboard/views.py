import datetime
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import login
from pages.models import CustomUser
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404, redirect
from pages.models import Categorie, Offre, Categorie, Promotion, Message, Reservation
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from django.contrib import messages
from pages.decorators import require_admin

@require_admin
def accuile_page(request):
    reservations = Reservation.objects.all()
    current_month = 0
    last_month = 0
    current_month_revenue = 0
    last_month_revenue = 0
    today_revenue = 0
    yesterday_revenue = 0
    today_reservations = 0
    yesterday_reservations = 0

    now = datetime.datetime.now()
    for reservation in reservations:
        reservation.status = reservation.offre.date_debut > reservation.date

        if reservation.date.month == now.month:
            current_month += 1
            current_month_revenue += reservation.offre.prix
        elif reservation.date.month == now.month - 1:
            last_month += 1
            last_month_revenue += reservation.offre.prix

        if reservation.date.day == now.day:
            today_revenue += reservation.offre.prix
            today_reservations += 1
        elif reservation.date.day == now.day - 1:
            yesterday_revenue += reservation.offre.prix
            yesterday_reservations += 1
    
    #calculate the monthly and daily growth (' calculations in total)
    reservations_monthly_growth = (current_month - last_month) / last_month * 100 if last_month != 0 else 100
    revenu_monthly_growth = (current_month_revenue - last_month_revenue) / last_month_revenue * 100 if last_month_revenue != 0 else 100
    reservations_daily_growth = (today_reservations - yesterday_reservations) / yesterday_reservations * 100 if yesterday_reservations != 0 else 100
    revenu_daily_growth = (today_revenue - yesterday_revenue) / yesterday_revenue * 100 if yesterday_revenue != 0 else 100

    reservations = sorted(reservations, key=lambda x: x.status, reverse=True)

    return render(request, 'admindashboard/index.html', {
        'reservations': reservations,
        'current_month': current_month,
        'current_month_revenue': current_month_revenue,
        'today_reservations': today_reservations,
        'today_revenue': today_revenue,
        'reservations_monthly_growth': reservations_monthly_growth,
        'revenu_monthly_growth': revenu_monthly_growth,
        'reservations_daily_growth': reservations_daily_growth,
        'revenu_daily_growth': revenu_daily_growth,
    })

@require_admin
def category_page(request) :
    categories = Categorie.objects.all()
    return render(request,'admindashboard/category.html', {'categories': categories})

@require_admin
def client_page(request):
    clients = CustomUser.objects.filter(is_staff=False).order_by('-id')
    return render(request, 'admindashboard/client.html', {'clients': clients})

@require_admin
def newclient_page(request) :
    return render(request,'admindashboard/newclient.html')

@require_admin
def contactus_page(request) :
    message = Message.objects.all()
    return render(request,'admindashboard/contactus.html', {'message': message})

@require_admin
def send_message_to_client(request) :
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        subject = "ِContact Us"
        from_email = "med@mail.com"  # Replace with your email
        to_email = [email]

        html_message = render_to_string('message_to_client.html', {'message': message, 'name': name})

        email_message = EmailMessage(
            subject=subject,
            body=html_message,  # HTML content goes here
            from_email=from_email,
            to=to_email,
        )
        email_message.content_subtype = "html"
        email_message.send()
        messages.info(request,"Message sent successfully")
        message = Message.objects.all()
        return render(request,'admindashboard/contactus.html', {'message': message})
    message = Message.objects.all()
    return render(request,'admindashboard/contactus.html', {'message': message})

@require_admin
def newcategory_page(request) :
    return render(request,'admindashboard/newcategory.html')

@require_admin
def newoffer_page(request) :
    categories = Categorie.objects.all()
    promotions = Promotion.objects.all()
    return render(request,'admindashboard/newoffer.html', {'categories': categories, 'promotions': promotions})
@require_admin
def offers_page(request) :
    filters = {
        'search': request.GET.get('search')
    }
    offers_unfiltered = Offre.objects.all()
    offers = []
    for offer in offers_unfiltered:
        if filters['search'] and filters['search'].lower() not in offer.titre.lower():
            continue
        offers.append(offer)
    
    categories = Categorie.objects.all()
    promotions = Promotion.objects.all()
    return render(request,'admindashboard/offers.html', {'offers': offers, 'categories': categories, 'promotions': promotions, 'filters':filters})
@require_admin
def promotion_page(request) :
    promotions = Promotion.objects.all()
    return render(request,'admindashboard/promotion.html', {'promotions': promotions})
@require_admin
def newpromotion_page(request) :
    return render(request,'admindashboard/newpromotion.html')
@require_admin
def settings_page(request) :
    return render(request,'admindashboard/settings.html')

@require_admin
def create_client(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        is_active = request.POST.get('is_active') == 'on'
        user = CustomUser.objects.create(
            email=email,
            password=make_password(password),
            first_name=first_name,
            last_name=last_name,
            is_staff=False,
            is_active=is_active,
        )
        return HttpResponseRedirect('client')
    else:
        return redirect('newclient')
@require_admin
def delete_client(request, client_id):
    client = get_object_or_404(CustomUser, id=client_id)
    client.delete()
    return redirect('client')
@require_admin
def edit_client(request, client_id):
    client = get_object_or_404(CustomUser, id=client_id)
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        user_type = request.POST.get('user_type')
        is_staff = True if user_type == 'admin' else False
        is_active = request.POST.get('is_active') == 'on'
        client.email = email
        client.password = make_password(password)
        client.first_name = first_name
        client.last_name = last_name
        client.is_staff = is_staff
        client.is_active = is_active
        client.save()
        return redirect('client')
    else:
        return redirect('client')

@require_admin
def create_category(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        categorie = Categorie.objects.create(
            nom=nom,
            description=description,
            image=image,
        )
        return HttpResponseRedirect('category')
    else:
        return redirect('newcategory')
@require_admin
def edit_category(request, category_id):
    category = get_object_or_404(Categorie, id=category_id)
    if request.method == 'POST':
        nom = request.POST.get('nom')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        category.nom = nom
        category.description = description
        category.image = image
        category.save()
        return redirect('category')
    else:
        return redirect('category')
@require_admin
def delete_category(request, category_id):
    category = get_object_or_404(Categorie, id=category_id)
    category.delete()
    return redirect('category')

@require_admin
def create_offer(request):
    if request.method == 'POST':
        titre = request.POST.get('titre')
        description = request.POST.get('description')
        prix = request.POST.get('prix')
        lieu = request.POST.get('lieu')
        capacite = request.POST.get('capacité')
        image = request.FILES.get('image')
        date_debut = request.POST.get('date_debut')
        date_fin = request.POST.get('date_fin')
        categorie_id = request.POST.get('categorie')
        promotion_id = request.POST.get('promotion')
        categorie = Categorie.objects.get(id=categorie_id) if categorie_id else None
        promotion = Promotion.objects.get(id=promotion_id) if promotion_id else None
        offre = Offre.objects.create(
            titre=titre,
            description=description,
            prix=prix,
            lieu=lieu,
            capacite=capacite,
            image=image,
            date_debut=date_debut,
            date_fin=date_fin,
            categorie=categorie,
            promotion=promotion,
        )
        return HttpResponseRedirect('offers')
    else:
        return redirect('newoffer')
@require_admin
def edit_offer(request, offer_id):
    offre = get_object_or_404(Offre, id=offer_id)
    if request.method == 'POST':
        titre = request.POST.get('titre')
        description = request.POST.get('description')
        prix = request.POST.get('prix')
        lieu = request.POST.get('lieu')
        capacite = request.POST.get('capacité')
        image = request.FILES.get('image')
        date_debut = request.POST.get('date_debut')
        date_fin = request.POST.get('date_fin')
        categorie_id = request.POST.get('categorie')
        promotion_id = request.POST.get('promotion')
        categorie = Categorie.objects.get(id=categorie_id) if categorie_id else None
        promotion = Promotion.objects.get(id=promotion_id) if promotion_id else None
        offre.titre = titre
        offre.description = description
        offre.prix = prix
        offre.lieu = lieu
        offre.capacite = capacite
        offre.image = image
        offre.date_debut = date_debut
        offre.date_fin = date_fin
        offre.categorie = categorie
        offre.promotion = promotion
        offre.save()
        return redirect('offers')
    else:
        return redirect('offers')
@require_admin
def delete_offer(request, offer_id):
    offre = get_object_or_404(Offre, id=offer_id)
    offre.delete()
    return redirect('offers')
@require_admin
def create_promotion(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        description = request.POST.get('description')
        remise = request.POST.get('remise')
        date_debut = request.POST.get('date_debut')
        date_fin = request.POST.get('date_fin')
        promotion = Promotion.objects.create(
            nom=nom,
            description=description,
            remise=remise,
            date_debut=date_debut,
            date_fin=date_fin,
        )
        promotion.save()
        return HttpResponseRedirect('promotion')
    else:
        return redirect('newpromotion')
@require_admin
def edit_promotion(request, promotion_id):
    promotion = Promotion.objects.get(id=promotion_id)
    if request.method == 'POST':
        promotion.nom = request.POST.get('nom')
        promotion.description = request.POST.get('description')
        promotion.remise = request.POST.get('remise')
        promotion.date_debut = request.POST.get('date_debut')
        promotion.date_fin = request.POST.get('date_fin')
        promotion.save()
        return redirect('promotion')
    else:
        return redirect('promotion')
@require_admin    
def delete_promotion(request, promotion_id):
    promotion = get_object_or_404(Promotion, id=promotion_id)
    promotion.delete()
    return redirect('promotion')
# Create your views here.
