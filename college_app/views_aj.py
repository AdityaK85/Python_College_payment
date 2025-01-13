import json
import random
import traceback
from django.http import JsonResponse
from django.shortcuts import redirect

from Project_utilty.decorators import handle_ajax_exception
from Project_utilty.phonepe import Payment, Payment_Request, Save_TransactionDetails, checkPhonePayStatus
# from Project_utilty.Utility import Payment
# from Project_utilty.decorators import get_date_label, handle_ajax_exception, is_admin_authenticated, is_authenticated
# from Project_utilty.send_emails import send_html_email
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
import datetime
from datetime import datetime, time, timedelta 
from django.db.models import Sum


@csrf_exempt
def login_handler(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    login_by = request.POST.get("login_by")
    login_obj = None
    if login_by == 'admin':
        login_obj = AdminMaster.objects.filter(username = username , password = password).last()
        url = '/admin_user/student_list/'
    else :
        login_obj = StudentMaster.objects.filter(student_id = username , student_password = password).last()
        url = f'/student_details/{login_obj.id}'
    
    if login_obj:
        request.session['user_id'] = login_obj.id
        request.session['user_type'] = "admin" if login_by == 'admin' else "student"
        return JsonResponse({"status": 1, "msg": "Login Successfully...", "url": url})
    else:
        return JsonResponse({"status": 0, "msg": "Invalid Credentials"})

@csrf_exempt
def logout(request):
    try :
        if request.session.get("user_id") :
            del request.session['user_id']
            del request.session['user_type']
    except :
        traceback.print_exc()
    return redirect('/login')



# @csrf_exempt
# @handle_ajax_exception
# def make_payment_aj(request):
#     id = request.POST.get('id')
#     amt = request.POST.get('amt')
#     amount = round((float(amt)))    
#     amount = amount * 100
#     REDIRECT_URL = f'http://127.0.0.1:8000/student_details'
#     response = Payment(amount, REDIRECT_URL , REDIRECT_URL, '8530926168' )
#     phonepe_redirecturl = ""
#     if response[0] == False:
#         return JsonResponse({'stutus':"0","msg":response[1]})
#     else:
#         response = json.loads(response[1])
#         phonepe_redirecturl = response['data']["instrumentResponse"]["redirectInfo"]["url"] 

#     send_data = {'status':1, 'msg':'Payment Successed' , 'phonepe_redirecturl': phonepe_redirecturl  }
#     return JsonResponse(send_data)

@csrf_exempt
@handle_ajax_exception
def make_payment_aj(request):
    data = request.POST.dict()
    id = request.POST.get('id')
    course_id = request.POST.get('course_id')
    email = request.POST.get('email')
    name = request.POST.get('name')
    mobile_no = request.POST.get("mobile_no")
    # address = request.POST.get('address')
    country = request.POST.get('country')
    state = request.POST.get('state')

    c_name = request.POST.get('c_name')
    c_type = request.POST.get('c_type')

    actual_amount = request.POST.get("actual_amount")
    plan_amount = request.POST.get('plan_amount')
    gst_amount = request.POST.get('gst_amount')
    discount_value = request.POST.get('discount_value')
    subscription_type = request.POST.get("subscription_type")
    payable_amount = request.POST.get("amt")
    payment_type = request.POST.get("payment_type")
    duration = request.POST.get("duration")
    plan_name = request.POST.get('plan_name')

    receipt = request.FILES.get("receipt")
    
    print('--------course_id------------ajax-----', course_id)

    transaction_id = f"TRANSID{random.randint(1000000000000, 9999999999000)}"
    while SubscriptionTable.objects.filter(transaction_id=transaction_id).exists():
        transaction_id = f"TRANSID{random.randint(1000000000000, 9999999999000)}"
    merchantuser_id = f"USERID{random.randint(1000000000000, 9999999999000)}"
    while SubscriptionTable.objects.filter(merchantuser_id=merchantuser_id).exists():
        merchantuser_id = f"USERID{random.randint(1000000000000, 9999999999000)}"

    
    redirect_url = f"{request.build_absolute_uri().rsplit('/', 2)[0]}/phonepe_payment_redirect/"    # redirect url 
    callback_url = f"{request.build_absolute_uri().rsplit('/', 2)[0]}/phonepe_callback_redirect/"  # callback url 
    amount = round((float(payable_amount)))
    
    amount = amount * 100
    request.session['subscription_type'] = subscription_type
    phonepe_redirecturl = ""
    user_obj = StudentMaster.objects.filter(id = id).last()
    phone_payment_status = ""
    response = Payment_Request(amount,transaction_id,merchantuser_id,redirect_url,callback_url) # call phone pe payment function
    print("::::response ::::", response)
    if response[0] == False:
        return JsonResponse({'stutus':0,"msg":response[1]})
    else:
        response = json.loads(response[1])

        request.session['transaction_id'] = transaction_id   # set transaction id on session
        request.session['isPaymentInitiated'] = 'Yes'   # set transaction id on session    
        
        
        phonepe_redirecturl = response['data']["instrumentResponse"]["redirectInfo"]["url"]
        phone_payment_status = "PAYMENT_PENDING"
    print("-------------------course_id-------", course_id)
    Save_TransactionDetails(request,user_obj,transaction_id,merchantuser_id,payment_type,payable_amount,None,phone_payment_status,None,duration,subscription_type,c_type,c_name,plan_name,course_id,plan_amount,gst_amount,actual_amount,receipt)
    return JsonResponse({'status':1,"msg":"Success","phonepe_redirecturl":phonepe_redirecturl})


@csrf_exempt
@handle_ajax_exception
def remove_payment_session(request):
    data = {}
    transaction_id = None
    try:
        transaction_id = request.session.get("transaction_id")
        isPaymentInitiated = request.session.get("isPaymentInitiated")

        del request.session['transaction_id']
        del request.session['isPaymentInitiated']
    except:
        pass
        traceback.print_exc()

    

    if not SubscriptionTable.objects.filter(transaction_id = transaction_id).exists():
        return JsonResponse({'status':'0',"msg":"Invalid transaction id."})
    
    next_time = (datetime.now()+ timedelta(minutes=1)).time()

    while datetime.now().time() < next_time:
        func_status,response = checkPhonePayStatus(transaction_id)
        print("***********",func_status,response)
        if func_status == True:
            
            
            if response['code'] == "PAYMENT_SUCCESS":
                providerReferenceId = response['data']['transactionId']
                payment_status = response['code']
                transaction_id = response['data']['merchantTransactionId']
                # checksum = response['checksum']

                Save_TransactionDetails(request,None,transaction_id,None,None, None,providerReferenceId,payment_status,"",None,None,None,None,None,None,None,None,FromRedirect=True)
                
                data = {'status':"1","msg":"Your payment was successful! Thank you for your payment"}
                break
            elif response['code'] == "PAYMENT_PENDING":
                # print("payment status---:",response['code'])
                data = {"status":"2","msg":"Your payment is currently being processed. You will receive a notification via email once the payment is complete."}

            elif response['code'] == "PAYMENT_ERROR":
                # print("payment status---:",response['code'])
                Save_TransactionDetails(request,None,transaction_id,None,None, None,None,"PAYMENT_ERROR",None,None,None,None,None,None,None,None,None)
                data = {'status':"0","msg":"Unfortunately, your payment could not be processed,Please check your payment information and try again."}
                break

            elif response['code'] == "INTERNAL_SERVER_ERROR":
                print("payment status---:",response['code'])

            else:
                print("-----------------------------",response['code'])
                Save_TransactionDetails(request,None,transaction_id,None,None, None,None,"PAYMENT_ERROR",None,None,None,None,None,None,None,None,None)
                data = {'status':"0","msg":"Something went wrong."}
                break
        else:
            # msg = response['message']
            Save_TransactionDetails(request,None,transaction_id,None,None, None,None,"PAYMENT_ERROR",None,None,None,None,None,None,None,None,None)
            data = {'status':"0","msg":"Something went wrong."}
            break
        
        time.sleep(0.6)
    
    return JsonResponse(data)


@csrf_exempt
@handle_ajax_exception
def phonepe_payment_redirect(request):
    response = request.POST.dict()
    providerReferenceId = response['providerReferenceId']
    payment_status = response['code']
    transaction_id = response['transactionId']
    checksum = response['checksum']
    get_usr = SubscriptionTable.objects.filter(transaction_id = transaction_id).last()
    Save_TransactionDetails(request,None,transaction_id,None,None, None,providerReferenceId,payment_status,checksum,None,None,None,None,None,None,None,None,FromRedirect=True, update_bal = True)
    return redirect(f'/student_details/{get_usr.fk_user.id}')


@csrf_exempt
@handle_ajax_exception
def phonepe_callback_redirect(request):
    
    return redirect('/')

import random

@csrf_exempt
@handle_ajax_exception
def save_student(request):
    student_name = request.POST.get('student_name')
    dob = datetime.strptime(request.POST.get('dob'), "%Y-%m-%d").date()
    gender = request.POST.get('gender')
    nationality = request.POST.get('nationality')
    email = request.POST.get('email') 
    mobile_no = request.POST.get('mobile_no')
    plan_id = request.POST.get('plan_id')
    course_fees = request.POST.get('course_fees') 
    print('----------plan_id------', plan_id)
    student_id = f'RDC_{random.randint(1111,9999)}'
    password = f'PASS{random.randint(1111,9999)}'

    StudentMaster.objects.create(   
        student_id = student_id,
        student_name = student_name,
        student_password = password,
        fk_course_id = plan_id,
        payble_amount = course_fees,
        dob = dob,
        gender = gender,
        nationality = nationality,
        email = email,
        mobile_no = mobile_no,
    )

    return JsonResponse({'status': 1})