from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(AdminMaster)
class AdminMasterAdmin(admin.ModelAdmin):
    list_display=['id','username','password']

@admin.register(CourseMaster)
class CourseMasterAdmin(admin.ModelAdmin):
    list_display=['id','course_name','course_fees','course_duration']

@admin.register(StudentMaster)
class StudentMasterAdmin(admin.ModelAdmin):
    list_display=['id', 'student_id', 'student_name', 'student_password', 'fk_course','payble_amount', 'created_dt']

@admin.register(PaymentMaster)
class PaymentMasterAdmin(admin.ModelAdmin):
    list_display=['id','fk_student','paid_amount','created_dt']

@admin.register(SubscriptionTable)
class SubscriptionTableAdmin(admin.ModelAdmin):
    list_display=['id','fk_user','order_id','transaction_id', 'merchantuser_id', 'provider_referenceid', 'checksum', 'actual_amount', 'plan_amount', 'gst_amount','payable_amount', 'discount_amount', 'phonepe_status', 'payment_status', 'payment_type', 'transaction_date']