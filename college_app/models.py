from django.db import models
from django.utils import timezone

# Create your models here.

class AdminMaster(models.Model):
    username = models.CharField(max_length=100, null=True,blank=True)
    password = models.CharField(max_length=100, null=True,blank=True)


class CourseMaster(models.Model):
    course_name = models.CharField(max_length=200, blank=True, null=True)
    course_fees = models.FloatField(blank=True, null=True)
    course_duration = models.CharField(max_length=200, blank=True, null=True)

class StudentMaster(models.Model):
    student_id = models.CharField(max_length=200, blank=True, null=True)
    student_name = models.CharField(max_length=200, blank=True, null=True)
    student_password = models.CharField(max_length=200, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=200, blank=True, null=True)
    nationality = models.CharField(max_length=200, blank=True, null=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    mobile_no = models.CharField(max_length=200, blank=True, null=True)
    fk_course = models.ForeignKey(CourseMaster,  on_delete=models.CASCADE,  blank=True, null=True)
    payble_amount = models.FloatField(blank=True, null=True)
    created_dt = models.DateTimeField(null=True,blank=True, default=timezone.now)

class PaymentMaster(models.Model):
    fk_student = models.ForeignKey(StudentMaster,  on_delete=models.CASCADE,  blank=True, null=True)
    paid_amount = models.FloatField(blank=True, null=True)
    created_dt = models.DateTimeField(null=True,blank=True)


class SubscriptionTable(models.Model):
    PAYEMENT_STATUS = (
		("PENDING", "PENDING"),
		("SUCCESS", "SUCCESS"),
        ("FAILED", "FAILED"),
        ("CANCELLED", "CANCELLED"),
        
	)

    fk_user = models.ForeignKey(StudentMaster,on_delete= models.CASCADE,blank=True,null=True)
    order_id = models.CharField(max_length= 200 , blank=True , null=True)
    transaction_id = models.CharField(max_length= 200 , blank=True , null=True)
    fk_course = models.ForeignKey(CourseMaster,  on_delete=models.CASCADE,  blank=True, null=True)
    
    merchantuser_id = models.CharField(max_length= 200 , blank= True ,null= True)
    provider_referenceid = models.CharField(max_length= 1000 , blank= True , null= True)
    checksum = models.CharField(max_length= 1000 , blank=True , null= True)

    actual_amount = models.FloatField(blank= True , null= True)
    plan_amount = models.FloatField(blank= True , null= True)
    gst_amount = models.FloatField(blank= True ,null= True)
    payable_amount = models.FloatField(blank= True ,null= True)
    discount_amount = models.FloatField(default= 0, blank= True ,null= True)

    phonepe_status = models.CharField(max_length= 200 , blank= True , null=True)
    payment_status = models.CharField(max_length= 200 , choices = PAYEMENT_STATUS,default="PENDING")
    payment_type = models.CharField(max_length=100 , blank= True , null= True)   # PHONEPE , DIRECT BANK TRANSFER, MANUAL
    transaction_date = models.DateTimeField(blank= True , null= True)