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
            $('#result').text("result: "+response.result);
            $('#result').show();
            $('#5next').show();
        },
        error: function(rs, e) {
            alert(e);
        }
    }); 
});

$('#1next').on('click', function () {
    $('#step2').show();
    $(this).hide();
});

$('#2next').on('click', function () {
    $('#step3').show();
    $(this).hide();
});

$('#3next').on('click', function () {
    $('#step4').show();
    $(this).hide();
});

$('#4next').on('click', function () {
    $('#step5').show();
    $(this).hide();
});

$('#5next').on('click', function () {
    $('#step6').show();
    $(this).hide();
});

$('#6next').on('click', function () {
    $('#step7').show();
    $(this).hide();
});

$('#see_details').on('click', function () {
    $('#details').show();
    $('#brief').hide();
});

$('#hide_details').on('click', function () {
    $('#details').hide();
    $('#brief').show();
});