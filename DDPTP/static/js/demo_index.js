// function predict(event){
//     action = event.data.action;
//     csrfmiddlewaretoken = event.data.csrf_token;
//     delete event.data.action;
//     delete event.data.csrf_token;
//     alert(event.data.account_status);
//     $.ajax({
//         type: "POST",
//         url: "/demo/index/predict",
//         data: {'action': action, 'csrfmiddlewaretoken': csrfmiddlewaretoken, 'information': event.data},
//         dataType: "json",
//         success: event.data.on_success,
//         error: function(rs, e) {
//             alert(e);
//         }
//     }); 
// }

// $('#predict').click({action: "predict", csrf_token: $('#csrf_token').val(), 
//                     account_status: $('#account_status').val(), duration: $('#duration').val(), credit_history: $('#credit_history').val(), purpose: $('#purpose').val(), 
//                     credit_amount: $('#credit_amount').val(), savings_account: $('#savings_account').val(), present_employment_since: $('#present_employment_since').val(), 
//                     installment_rate_in_income: $('#installment_rate_in_income').val(), guarantors: $('#guarantors').val(), present_residence_since: $('#present_residence_since').val(),
//                     other_installment_plans: $('#other_installment_plans').val(), housing: $('#housing').val(), existing_credits: $('#existing_credits').val(), job: $('#job').val(),
//                     maintenance_provider_number: $('#maintenance_provider_number').val(), telephone: $('#telephone').val(), foreign_worker: $('#foreign_worker').val(),
//     on_success: function(response){
//         $('#result').text("result: True");
//         $('#result').show();
// }}, predict);

$('#predict').on('click', function () {
    $.ajax({
        type: "POST",
        url: "/demo/index/predict",
        data: {action: "predict", csrfmiddlewaretoken: $('#csrf_token').val(), account_status: $('#account_status').val(), duration: $('#duration').val(), credit_history: $('#credit_history').val(), purpose: $('#purpose').val(), 
        credit_amount: $('#credit_amount').val(), savings_account: $('#savings_account').val(), present_employment_since: $('#present_employment_since').val(), 
        installment_rate_in_income: $('#installment_rate_in_income').val(), guarantors: $('#guarantors').val(), present_residence_since: $('#present_residence_since').val(),
        other_installment_plans: $('#other_installment_plans').val(), housing: $('#housing').val(), existing_credits: $('#existing_credits').val(), job: $('#job').val(),
        maintenance_provider_number: $('#maintenance_provider_number').val(), telephone: $('#telephone').val(), foreign_worker: $('#foreign_worker').val()},
        dataType: "json",
        success: function(response){
            $('#result').text("result: True");
            $('#result').show();
        },
        error: function(rs, e) {
            alert(e);
        }
    }); 
});
