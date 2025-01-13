import {log, callAjax, sweetAlertMsg, showToastMsg} from '../CommonJS/common.js';

$("#postions").addClass("active");


window.change_course = async function(course_id) {
    if (course_id != "") {
        var response = await callAjax('/get_course', {'course_id': course_id})
        if (response.status == 1){
            log(response)
            $('#coures_duration').val(response.duration)
            $('#coures_fees').val(response.fees)
        }
        else {
            $('#coures_duration').val('')
            $('#coures_fees').val('')
        }
    }
    else {
        $('#coures_duration').val('')
        $('#coures_fees').val('')
    }
}


window.SaveStudent = async function(this_) {
    var student_name = $("#student_name").val()
    var dob = $("#dob").val()
    var gender = $("#gender").val()
    var nationality = $("#nationality").val()
    var email = $("#email").val()
    var mobile_no = $("#mobile_no").val()
    var plan_id = $("#plan_id").val()
    var coures_fees = $("#coures_fees").val()

    var data = {
        'student_name' : student_name,
        'dob' : dob,
        'gender' : gender,
        'nationality' : nationality,
        'email' : email,
        'mobile_no'  : mobile_no,
        'plan_id' : plan_id,
        'course_fees' : coures_fees
    }

    var response = await callAjax('/save_student/', data , this_, 'Saving', 'Save', false )
    if (response.status == 1) {
        location.reload()
    }
    else {
        await sweetAlertMsg('Something went wrong', 'Having some error occured while registering new student', 'error')
    }
}
