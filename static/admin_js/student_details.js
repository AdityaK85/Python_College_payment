import { log, callAjax, sweetAlertMsg, showToastMsg } from '../CommonJS/common.js';

window.openPaymentModal = function(total_amount, sutd_id, course_id){
    $("#student_id").val(sutd_id)
    $("#course_id").val(course_id)
    $("#total_amount").html(total_amount)
    $("#basicModal").modal('show')
    var course_id = $("#course_id").val()
    log("------------",course_id)
}

window.make_payment = async function()
{   
    var student_id = $("#student_id").val()
    var pay_amount = $("#pay_amount").val()
    var course_id = $("#course_id").val()

    if (pay_amount.trim() == ""){
        showToastMsg('Amount', 'Please enter payment amount', 'error')
        return ;
    }

    var data = {
        'id': student_id,
        'amt': pay_amount,
        'course_id': course_id
    }
    var response = await callAjax('/make_payment_aj/', data );
    if (response.status == 1)
    {
        location.href = response.phonepe_redirecturl
    }
    else 
    {
        showToastMsg("Error", response.msg, 'error');
    }
}

window.cod_payment = async function(id )
{   
    var data = {
        'id': id,
    }
    var response = await callAjax('/cod_payment_aj/', data );
    if (response.status == 1)
    {
        showToastMsg("Success", response.msg, 'success');
        await new Promise(resolve => setTimeout(resolve, 1500)); 
        location.reload();
    }
    else 
    {
        showToastMsg("Error", response.msg, 'error');
    }
}




$(document).ready(async () => {
    var isPayment = $("#payment_status").val();
    log("-------ispayment------", isPayment)
    if (isPayment == 'Yes')
    {
        
        $("#payment_modal").modal("show");
        var response = await callAjax('/remove_payment_session/',{});
		$("#payment_modal").css("display","none");
		
		console.log(response)
        if (response.status == "1")
        {
            
            
            await sweetAlertMsg('SUCCESS', 'Payment successful! Thank you for your payment.', 'success');
            
            location.reload();   
        }
		else if (response.status == "2")
        {
            
            
            await sweetAlertMsg('Information', response.msg, 'info');
            
            location.reload();   
        }
        else
        {
            await sweetAlertMsg('Error', response.msg, 'error');
            location.reload();   
        }
    }
    
})