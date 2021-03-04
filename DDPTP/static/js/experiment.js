e2_t1_q1_original_result = NaN;
e2_t1_q2_original_result = NaN;
e2_t1_q1_dp_result = NaN;
e2_t1_q2_dp_result = NaN;
new_count = NaN;
e2_t1_q3_original_result = NaN;
e2_t1_q4_original_result = NaN;
e2_t1_q3_dp_result = NaN;
e2_t1_q4_dp_result = NaN;
new_count_small = NaN;
e2_t1_q5_original_result = NaN;
e2_t1_q6_original_result = NaN;
e2_t1_q5_dp_result = NaN;
e2_t1_q6_dp_result = NaN;

function run_query(event){
    $.ajax({
        type: "POST",
        url: "/experiments/run",
        data: {'action': event.data.action, 'csrfmiddlewaretoken': event.data.csrf_token},
        dataType: "json",
        success: event.data.on_success,
        error: function(rs, e) {
            alert(e);
        }
    }); 
}

function hide_or_show(event){
    if($('#'+event.data.button).val() == "show"){
        $('#'+event.data.result_block).text(window[event.data.result_block]);
        $('#'+event.data.button).val("hide");
    }
    else if($('#'+event.data.button).val() == "hide"){
        $('#'+event.data.result_block).text("****");
        $('#'+event.data.button).val("show");
    }
}

$('#run_e1_d1').click({action: "run_e1_d1", csrf_token: $('#csrf_token').val(), on_success: function(response){
    $('#e1_d1_original_score').text(response.statlog_original_score);
    $('#e1_d1_processed_score').text(response.statlog_processed_score);
    $('#e1_d1_result').show();
}}, run_query);

$('#run_e1_d2').click({action: "run_e1_d2", csrf_token: $('#csrf_token').val(), on_success: function(response){
    $('#e1_d2_original_score').text(response.adult_original_score);
    $('#e1_d2_processed_score').text(response.adult_processed_score);
    $('#e1_d2_abstracted_score').text(response.adult_abstracted_score);
    $('#e1_d2_result').show();
}}, run_query);

$('#run_e2_t1_q1').click({action: "run_e2_t1_q1", csrf_token: $('#csrf_token').val(), on_success: function(response) {
    e2_t1_q1_original_result = response.original_result;
    e2_t1_q1_dp_result = response.dp_result;
    $('#e2_t1_q1_count').text(response.count);
    $('#e2_t1_q1_processed_result').text(response.dp_result);
    $('#e2_t1_q1_result').show();
}}, run_query);

$('#run_e2_t1_q2').click({action: "run_e2_t1_q2", csrf_token: $('#csrf_token').val(), on_success: function(response) {
    e2_t1_q2_original_result = response.original_result;
    e2_t1_q2_dp_result = response.dp_result;
    new_count = response.count;
    $('#e2_t1_q2_count').text(response.count);
    $('#e2_t1_q2_processed_result').text(response.dp_result);
    $('#e2_t1_q2_result').show();
    $('#e2_t1_c12').show();
}}, run_query);

$('#run_e2_t1_q3').click({action: "run_e2_t1_q3", csrf_token: $('#csrf_token').val(), on_success: function(response) {
    e2_t1_q3_original_result = response.original_result;
    e2_t1_q3_dp_result = response.dp_result;
    $('#e2_t1_q3_count').text(response.count);
    $('#e2_t1_q3_processed_result').text(response.dp_result);
    $('#e2_t1_q3_result').show();
}}, run_query);

$('#run_e2_t1_q4').click({action: "run_e2_t1_q4", csrf_token: $('#csrf_token').val(), on_success: function(response) {
    e2_t1_q4_original_result = response.original_result;
    e2_t1_q4_dp_result = response.dp_result;
    new_count_small = response.count;
    $('#e2_t1_q4_count').text(response.count);
    $('#e2_t1_q4_processed_result').text(response.dp_result);
    $('#e2_t1_q4_result').show();
    $('#e2_t1_c34').show();
}}, run_query);

$('#run_e2_t1_q5').click({action: "run_e2_t1_q5", csrf_token: $('#csrf_token').val(), on_success: function(response) {
    e2_t1_q5_original_result = response.original_result;
    e2_t1_q5_dp_result = response.dp_result;
    $('#e2_t1_q5_count').text(response.count);
    $('#e2_t1_q5_processed_result').text(response.dp_result);
    $('#e2_t1_q5_result').show();
}}, run_query);

$('#run_e2_t1_q6').click({action: "run_e2_t1_q6", csrf_token: $('#csrf_token').val(), on_success: function(response) {
    e2_t1_q6_original_result = response.original_result;
    e2_t1_q6_dp_result = response.dp_result;
    $('#e2_t1_q6_processed_result').text(response.dp_result);
    $('#e2_t1_q6_result').show();
    $('#e2_t1_c567').show();
}}, run_query);

$('#run_e2_t2_c1').click({action: "run_e2_t2_c1", csrf_token: $('#csrf_token').val(), on_success: function(response) {
    $('#e2_t2_c1_result').text("noise sum: "+response.noise_sum);
}}, run_query);

$('#run_e2_t2_c2').click({action: "run_e2_t2_c2", csrf_token: $('#csrf_token').val(), on_success: function(response) {
    $('#e2_t2_c2_result').text("noise sum: "+response.noise_sum);
}}, run_query);

$('#run_e3_t1').click({action: "run_e3_t1", csrf_token: $('#csrf_token').val(), on_success: function(response) {
    $('#e3_t1_m1_marital_status').text("Category 0: \n"+response.original_zero_rates.marital_status+"\n Category 1: \n"+response.original_one_rates.marital_status);
    $('#e3_t1_m1_sex').text("Category 0: \n"+response.original_zero_rates.sex+"\n Category 1: \n"+response.original_one_rates.sex);
    $('#e3_t1_m1_race').text("Category 0: \n"+response.original_zero_rates.race+"\n Category 1: \n"+response.original_one_rates.race);
    $('#e3_t1_m1_native_country').text("Category 0: \n"+response.original_zero_rates.native_country+"\n Category 1: \n"+response.original_one_rates.native_country);
    $('#e3_t1_m2_marital_status').text("Category 0: \n"+response.processed_zero_rates.marital_status+"\n Category 1: \n"+response.processed_one_rates.marital_status);
    $('#e3_t1_m2_sex').text("Category 0: \n"+response.processed_zero_rates.sex+"\n Category 1: \n"+response.processed_one_rates.sex);
    $('#e3_t1_m2_race').text("Category 0: \n"+response.processed_zero_rates.race+"\n Category 1: \n"+response.processed_one_rates.race);
    $('#e3_t1_m2_native_country').text("Category 0: \n"+response.processed_zero_rates.native_country+"\n Category 1: \n"+response.processed_one_rates.native_country);
    $('#e3_t1_m3_marital_status').text("Category 0: \n"+response.abstracted_zero_rates.marital_status+"\n Category 1: \n"+response.abstracted_one_rates.marital_status);
    $('#e3_t1_m3_sex').text("Category 0: \n"+response.abstracted_zero_rates.sex+"\n Category 1: \n"+response.abstracted_one_rates.sex);
    $('#e3_t1_m3_race').text("Category 0: \n"+response.abstracted_zero_rates.race+"\n Category 1: \n"+response.abstracted_one_rates.race);
    $('#e3_t1_m3_native_country').text("Category 0: \n"+response.abstracted_zero_rates.native_country+"\n Category 1: \n"+response.abstracted_one_rates.native_country);
}}, run_query);

$('#run_e3_t2').click({action: "run_e3_t2", csrf_token: $('#csrf_token').val(), on_success: function(response) {
    $('#e3_t2_m1_marital_status_and_sex').text("Category 0: \n"+response.original_zero_rates+"\n Category 1: \n"+response.original_one_rates);
    $('#e3_t2_m2_marital_status_and_sex').text("Category 0: \n"+response.processed_zero_rates+"\n Category 1: \n"+response.processed_one_rates);
}}, run_query);

$('#run_e2_t1_c1').click(function(){
    result = e2_t1_q2_original_result*new_count - e2_t1_q1_original_result*(new_count-1);
    $('#e2_t1_c1_result').text(e2_t1_q2_original_result+"*"+new_count+"-"+e2_t1_q1_original_result+"*("+new_count+"-1) = "+result);
})

$('#run_e2_t1_c2').click(function(){
    result = e2_t1_q2_dp_result*new_count - e2_t1_q1_dp_result*(new_count-1);
    $('#e2_t1_c2_result').text(e2_t1_q2_dp_result+"*"+new_count+"-"+e2_t1_q1_dp_result+"*("+new_count+"-1) = "+result);
})

$('#run_e2_t1_c6').click(function(){
    $.ajax({
        type: "POST",
        url: "/experiments/run",
        data: {'action': 'run_e2_t1_c6', 'csrfmiddlewaretoken': $('#csrf_token').val(), 'real_result': e2_t1_q5_original_result},
        dataType: "json",
        success: function(response) {
            $('#e2_t1_c6_result').text("correct rate: "+response.correct_rate);
        },
        error: function(rs, e) {
            alert(e);
        }
    }); 
})

$('#run_e2_t1_c7').click(function(){
    $.ajax({
        type: "POST",
        url: "/experiments/run",
        data: {'action': 'run_e2_t1_c7', 'csrfmiddlewaretoken': $('#csrf_token').val(), 'real_result': e2_t1_q5_original_result},
        dataType: "json",
        success: function(response) {
            $('#e2_t1_c7_result').text("correct rate: "+response.correct_rate);
        },
        error: function(rs, e) {
            alert(e);
        }
    }); 
})

$('#show_e2_t1_q1').click({button: "show_e2_t1_q1", result_block: "e2_t1_q1_original_result"}, hide_or_show);
$('#show_e2_t1_q2').click({button: "show_e2_t1_q2", result_block: "e2_t1_q2_original_result"}, hide_or_show);
$('#show_e2_t1_q3').click({button: "show_e2_t1_q3", result_block: "e2_t1_q3_original_result"}, hide_or_show);
$('#show_e2_t1_q4').click({button: "show_e2_t1_q4", result_block: "e2_t1_q4_original_result"}, hide_or_show);
$('#show_e2_t1_q5').click({button: "show_e2_t1_q5", result_block: "e2_t1_q5_original_result"}, hide_or_show);
$('#show_e2_t1_q6').click({button: "show_e2_t1_q6", result_block: "e2_t1_q6_original_result"}, hide_or_show);


$('#run_e2_t1_c3').click(function(){
    result = e2_t1_q4_original_result*new_count_small - e2_t1_q3_original_result*(new_count_small-1);
    $('#e2_t1_c3_result').text(e2_t1_q4_original_result+"*"+new_count_small+"-"+e2_t1_q3_original_result+"*("+new_count_small+"-1) = "+result);
})

$('#run_e2_t1_c4').click(function(){
    result = e2_t1_q4_dp_result*new_count_small - e2_t1_q3_dp_result*(new_count_small-1);
    $('#e2_t1_c4_result').text(e2_t1_q4_dp_result+"*"+new_count_small+"-"+e2_t1_q3_dp_result+"*("+new_count_small+"-1) = "+result);
})

$('#run_e2_t1_c5').click(function(){
    if(e2_t1_q6_dp_result>e2_t1_q5_dp_result){
        result = "The new entry is a single male";
    }
    else{
        result = "The new entry is not a single male";
    }
    $('#e2_t1_c5_result').text(result);
})