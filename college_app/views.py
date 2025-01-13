from django.shortcuts import render
from django.template.loader import render_to_string
from .models import *
from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_control
from Project_utilty.decorators import  handle_admin_page_exception
from django.db.models import Sum

# Create your views here.

def index(request):
    return render(request, 'html/index.html')

def login(request):
    return render(request, 'login.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@handle_admin_page_exception
def new_student(request, user):
    course_obj = CourseMaster.objects.all().order_by('-id')
    return render(request, 'html/new_student.html', {'course_obj': course_obj, 'user' : user})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@handle_admin_page_exception
def course_list(request, user):
    return render(request, 'html/course_list.html', {'user' : user})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@handle_admin_page_exception
def add_course(request, user):
    return render(request, 'html/add_course.html', {'user' : user})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@handle_admin_page_exception
def student_details(request,user, user_id):
    stud_obj = StudentMaster.objects.filter(id = user_id).last()
    transaction_obj = SubscriptionTable.objects.filter(fk_user = stud_obj).order_by('-id')

    if stud_obj:
        payble_amt = stud_obj.payble_amount
        total_paid = PaymentMaster.objects.filter(fk_student = stud_obj).aggregate(total_paid=Sum('paid_amount'))
        print("--------total_paid--", total_paid)

    return render(request, 'html/student_details.html', {'stud_obj': stud_obj , 'user_type': request.session.get('user_type') , 'transaction_obj': transaction_obj , 'total_paid':total_paid,  'user' : user})

def student_list(request):
    stu_obj = StudentMaster.objects.all().order_by('-id')
    # for i in stu_obj:
    #     paid_amount = PaymentMaster.objects.filter(fk_student_id = i.id)
    render_string = render_to_string('r_t_s_htmls/r_t_s_students.html', {'stu_obj': stu_obj})
    context = {'string': render_string}
    return render(request, 'html/student_list.html', context)

@csrf_exempt
def get_course(request):
    course_id = request.POST.get("course_id")
    obj = CourseMaster.objects.filter(id = course_id).last()
    duration, fees = None, None
    if obj:
        duration = obj.course_duration
        fees = obj.course_fees
    return JsonResponse({'status':1, 'duration':duration, 'fees':fees})