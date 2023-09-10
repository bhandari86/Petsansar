from django.urls import path

from petsansar import views

urlpatterns = [
    path('', views.index, name="index"),

    path('contact', views.contact, name="contact"),
    path('list', views.list, name="list"),
    path('signup', views.signup, name="signup"),

    path('login', views.handlelogin, name="handlelogin"),

    path('logout', views.handlelogout, name="handlelogout"),

    path('activate/<uidb64>/<token>', views.ActivateAccountView.as_view(), name="activate"),

    path('adoption', views.adopt, name="adoption"),
    path('aboutus', views.aboutus, name="aboutus"),
    path('dog', views.dog, name="dog"),
    path('blog', views.blog, name="blog"),
    path('rescue', views.rescue, name="rescue"),
    path('surrender', views.surrender, name="surrender"),
    path('search', views.search, name="search"),
    path('rescue-form', views.rescue_form, name="rescue_form"),

    path('thankyou', views.thankyou, name="thankyou"),

    path('animaldetails/<int:animal_id>', views.animaldetails, name="animaldetails"),
    path('animaldetails/<int:animal_id>/adopt/', views.adoption_request, name='adoption_request'),
    path('animaldetails/<int:animal_id>/adopt/submit', views.submit_adoption_request, name='submit_adoption_request'),

    path('animal_list/<int:animal_id>', views.list_request, name="list_request"),
    path('animal_list/<int:animal_id>/adopt/submit', views.submit_list_adoption_request, name="submit_list_adoption_request"),
    
    path('donation', views.donation, name="donation"),
    path('list/<int:ianimal_id>/approve/', views.approved_animal, name="approved_animal"),
    path('api/verify_payment', views.verify_payment, name="verify_payment"),

    path('adoption-stats', views.adoption_stats, name="adoption_stats"),
    path('surrender-stats', views.surrender_stats, name="surrender_stats"),

    path('adoption-map', views.adoption_map, name='adoption_map'),
    path('notifications', views.view_notifications, name='view_notifications')

    # path('adoption-request',views.adoption_request, name="adoption_request"),

]
