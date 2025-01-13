from django.urls import path
from .views import *
from .views_aj import *
from django.conf import settings
from django.conf.urls.static import static



nr_url = [
    path('', index),
    path('login/', login),
    path('logout/', logout),
    path('admin_user/student_list/', student_list),
    path('admin_user/new_student/', new_student),
    path('admin_user/course_list/', course_list),
    path('admin_user/add_course/', add_course),
    path('student_details/<int:user_id>', student_details),
] 

ajax_url = [
    path('get_course', get_course),
    path('login_handler/', login_handler),
    path('make_payment_aj/', make_payment_aj),
    path('remove_payment_session/', remove_payment_session),
    path('phonepe_payment_redirect/', phonepe_payment_redirect, name='phonepe_payment_redirect'),
    path('phonepe_callback_redirect/', phonepe_callback_redirect, name='phonepe_callback_redirect'),
    path('save_student/', save_student, name='phonepe_callback_redirect'),


] 


urlpatterns = [ *nr_url, *ajax_url ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)