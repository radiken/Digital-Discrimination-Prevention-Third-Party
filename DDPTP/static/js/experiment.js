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
e1_d2_customize_options = {};

function run_query(event){
    $(this).prop('value', 'Loading');
    $.ajax({
        type: "POST",
        url: "/experiments/run",
        data: {'action': event.data.action, 'csrfmiddlewaretoken': event.data.csrf_token},
        dataType: "json",
        success: event.data.on_success,
        error: function(rs, e) {
            alert("Unexpected error. Please refresh the page and try again or contact me through email.");
            $(this).prop('value', 'Run again');
        }
    }); 
}

function hide_or_show(event){
    if($('#'+event.data.button).val() == "Show"){
        $('#'+event.data.result_block).text(window[event.data.result_block]);
        $('#'+event.data.button).val("Hide");
    }
    else if($('#'+event.data.button).val() == "Hide"){
        $('#'+event.data.result_block).text("****");
        $('#'+event.data.button).val("Show");
    }
}

$('#run_e1_d1').click({action: "run_e1_d1", csrf_token: $('#csrf_token').val(), on_success: function(response){
    $('#e1_d1_result_scores').text("Original: "+response.metrics[0][0]+"; Customized: "+response.metrics[0][1]);
    draw_e1_d1_metrics(response.metrics);
    $('#e1_d1_result').show('fast');
    $('#run_e1_d1').val('Run again');
}}, run_query);

$('#run_e1_d2').click({action: "run_e1_d2", csrf_token: $('#csrf_token').val(), on_success: function(response){
    $('#e1_d2_result_scores').text("Original: "+response.metrics[0][0]+"; Customized: "+response.metrics[0][1]);
    draw_e1_d2_metrics(response.metrics);
    $('#e1_d2_result').show('fast');
    $('#run_e1_d2').val('Run again');
    $('#e1_d2_improvement').show('fast');
}}, run_query);

$('#run_e1_d2_improvement').click({action: "run_e1_d2_improvement", csrf_token: $('#csrf_token').val(), on_success: function(response){
    correlations = JSON.parse(response.correlations);
    colors = [];
    len = correlations["index"].length;
    i = 0;
    while(i < len){
        red = 255-i*(255/len);
        green = i*(255/len);
        color = 'rgba('+red+', '+green+', 0, 0.5)';
        colors.push(color);
        i++;
    }
    var element = $('#e1_d2_improvement_result_canvas');
    var chart = new Chart(element, {
        type: 'bar',
        data: {
            labels: correlations["index"],
            datasets: [{
                data: correlations["data"],
                backgroundColor: colors,
                borderColor: 'rgba(200, 200, 200, 0.75)',
                borderWidth: 1
            }]
        },
        options: {
            maintainAspectRatio: false,
            title: {display: true, text: "Sum of absolute correlations of sex and race"},
            scales: {yAxes: [{ticks: {suggestedMin: 0, suggestedMax: 1}}]},
        }
    });
    $('#e1_d2_improvement_result').show('fast');
    $('#run_e1_d2_improvement').val('Run again');
    $('#e1_d2_improved').show('fast');
}}, run_query);

$('#run_e1_d2_improved').click({action: "run_e1_d2_improved", csrf_token: $('#csrf_token').val(), on_success: function(response){
    $('#e1_d2_improved_result_scores').text("Original: "+response.metrics[0][0]+"; Customized: "+response.metrics[0][1]);
    draw_e1_d2_improved_metrics(response.metrics);
    $('#e1_d2_improved_result').show('fast');
    $('#run_e1_d2_improved').val('Run again');
}}, run_query);

$('#run_e2_t1_q1').click({action: "run_e2_t1_q1", csrf_token: $('#csrf_token').val(), on_success: function(response) {
    e2_t1_q1_original_result = response.original_result;
    e2_t1_q1_dp_result = response.dp_result;
    $('#e2_t1_q1_count').text(response.count);
    $('#e2_t1_q1_processed_result').text(response.dp_result);
    $('#e2_t1_q1_result').show('fast');
    $('#run_e2_t1_q1').val('Run again');
    $('#e2_t1_q2').show('fast');
}}, run_query);

$('#run_e2_t1_q2').click({action: "run_e2_t1_q2", csrf_token: $('#csrf_token').val(), on_success: function(response) {
    e2_t1_q2_original_result = response.original_result;
    e2_t1_q2_dp_result = response.dp_result;
    new_count = response.count;
    $('#e2_t1_q2_count').text(response.count);
    $('#e2_t1_q2_processed_result').text(response.dp_result);
    $('#e2_t1_q2_result').show('fast');
    $('#e2_t1_c12').show('fast');
    $('#run_e2_t1_q2').val('Run again');
}}, run_query);

$('#run_e2_t1_q3').click({action: "run_e2_t1_q3", csrf_token: $('#csrf_token').val(), on_success: function(response) {
    e2_t1_q3_original_result = response.original_result;
    e2_t1_q3_dp_result = response.dp_result;
    $('#e2_t1_q3_count').text(response.count);
    $('#e2_t1_q3_processed_result').text(response.dp_result);
    $('#e2_t1_q3_result').show('fast');
    $('#run_e2_t1_q3').val('Run again');
    $('#e2_t1_q4').show('fast');
}}, run_query);

$('#run_e2_t1_q4').click({action: "run_e2_t1_q4", csrf_token: $('#csrf_token').val(), on_success: function(response) {
    e2_t1_q4_original_result = response.original_result;
    e2_t1_q4_dp_result = response.dp_result;
    new_count_small = response.count;
    $('#e2_t1_q4_count').text(response.count);
    $('#e2_t1_q4_processed_result').text(response.dp_result);
    $('#e2_t1_q4_result').show('fast');
    $('#e2_t1_c34').show('fast');
    $('#run_e2_t1_q4').val('Run again');
}}, run_query);

$('#run_e2_t1_q5').click({action: "run_e2_t1_q5", csrf_token: $('#csrf_token').val(), on_success: function(response) {
    e2_t1_q5_original_result = response.original_result;
    e2_t1_q5_dp_result = response.dp_result;
    $('#e2_t1_q5_count').text(response.count);
    $('#e2_t1_q5_processed_result').text(response.dp_result);
    $('#e2_t1_q5_result').show('fast');
    $('#run_e2_t1_q5').val('Run again');
    $('#e2_t1_q6').show('fast');
}}, run_query);

$('#run_e2_t1_q6').click({action: "run_e2_t1_q6", csrf_token: $('#csrf_token').val(), on_success: function(response) {
    e2_t1_q6_original_result = response.original_result;
    e2_t1_q6_dp_result = response.dp_result;
    $('#e2_t1_q6_processed_result').text(response.dp_result);
    $('#e2_t1_q6_result').show('fast');
    $('#e2_t1_c567').show('fast');
    $('#run_e2_t1_q6').val('Run again');
}}, run_query);

$('#run_e2_t2_c1').click({action: "run_e2_t2_c1", csrf_token: $('#csrf_token').val(), on_success: function(response) {
    $('#e2_t2_c1_result').text("noise sum: "+response.noise_sum);
    $('#e2_t2_c1_result').show('fast');
    $('#run_e2_t2_c1').val('compute again');
}}, run_query);

$('#run_e2_t2_c2').click({action: "run_e2_t2_c2", csrf_token: $('#csrf_token').val(), on_success: function(response) {
    $('#e2_t2_c2_result').text("noise sum: "+response.noise_sum).show('fast');
    $('#run_e2_t2_c2').val('compute again');
}}, run_query);

$('#run_e2_t1_c1').click(function(){
    result = e2_t1_q2_original_result*new_count - e2_t1_q1_original_result*(new_count-1);
    $('#e2_t1_c1_result').text(e2_t1_q2_original_result+"*"+new_count+"-"+e2_t1_q1_original_result+"*("+new_count+"-1) = "+result).show('fast');
})

$('#run_e2_t1_c2').click(function(){
    result = e2_t1_q2_dp_result*new_count - e2_t1_q1_dp_result*(new_count-1);
    $('#e2_t1_c2_result').text(e2_t1_q2_dp_result+"*"+new_count+"-"+e2_t1_q1_dp_result+"*("+new_count+"-1) = "+result).show('fast');
})

$('#run_e2_t1_c6').click(function(){
    $.ajax({
        type: "POST",
        url: "/experiments/run",
        data: {'action': 'run_e2_t1_c6', 'csrfmiddlewaretoken': $('#csrf_token').val(), 'real_result': e2_t1_q5_original_result},
        dataType: "json",
        success: function(response) {
            $('#e2_t1_c6_result').text("correct rate: "+response.correct_rate).show('fast');
        },
        error: function(rs, e) {
            alert("Unexpected error. Please refresh the page and try again or contact me through email.");
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
            $('#e2_t1_c7_result').text("correct rate: "+response.correct_rate).show('fast');
        },
        error: function(rs, e) {
            alert("Unexpected error. Please refresh the page and try again or contact me through email.");
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
    $('#e2_t1_c3_result').text(e2_t1_q4_original_result+"*"+new_count_small+"-"+e2_t1_q3_original_result+"*("+new_count_small+"-1) = "+result).show('fast');
})

$('#run_e2_t1_c4').click(function(){
    result = e2_t1_q4_dp_result*new_count_small - e2_t1_q3_dp_result*(new_count_small-1);
    $('#e2_t1_c4_result').text(e2_t1_q4_dp_result+"*"+new_count_small+"-"+e2_t1_q3_dp_result+"*("+new_count_small+"-1) = "+result).show('fast');
})

$('#run_e2_t1_c5').click(function(){
    if(e2_t1_q6_dp_result>e2_t1_q5_dp_result){
        result = "The new entry is a single male";
    }
    else{
        result = "The new entry is not a single male";
    }
    $('#e2_t1_c5_result').text(result).show('fast');
})

$('#run_e2_t2_customize').click(function(){
    $('#run_e2_t2_customize').val("Loading");
    epsilon = $("#e2_t2_customize_input").val();
    if(!isNaN(epsilon) | epsilon!=""){
        if(epsilon>0){
            $.ajax({
                type: "POST",
                url: "/experiments/run",
                data: {'action': 'run_e2_t2_customize', 'csrfmiddlewaretoken': $('#csrf_token').val(), 'epsilon': epsilon},
                dataType: "json",
                success: function(response) {
                    $('#e2_t2_customize_result').text("noise sum: "+response.noise_sum).show('fast');
                    $('#run_e2_t2_customize').val("Run again");
                },
                error: function(rs, e) {
                    alert("Unexpected error. Please refresh the page and try again or contact me through email.");
                    $('#run_e2_t2_customize').val("Run again");
                }
            }); 
        }
        else{
            alert("You must fill in a positive number!");
        }
    }
    else{
        alert("You must fill in a positive number!");
    }
})

statlog_continuous_attributes = ["duration", "credit_amount", "installment_rate_in_income", "present_residence_since", "age", "existing_credits", "maintenance_provider_number"];

$('#run_e1_d2_customize').click(function(){
    $('#run_e1_d2_customize').val("Loading");
    $('#e1_d2_customize_s2').children('div:visible').each(function(){
        attribute_name = $(this).attr('id');
        if(statlog_continuous_attributes.includes(attribute_name)){
            // continuous attribute
            limit = $(this).find(".continuous_abstraction_cn").text();
            e1_d2_customize_options[attribute_name] = ["<"+limit, ">="+limit];
        }
        else{
            // discrete attribute
            grouping = {}
            $("#"+attribute_name+"_abstraction_on").find("select").each(function(){
                group = $(this).val();
                if(group!="isolate"){
                    code = $(this).attr("id");
                    if(group in grouping){
                        grouping[group].push(code);
                    }
                    else{
                        grouping[group] = [code];
                    }
                }
            })
            e1_d2_customize_options[attribute_name] = grouping;
        }
    });
    classifier = $("#e1_d2_customize_classifier").val();
    $.ajax({
        type: "POST",
        url: "/experiments/run",
        data: {'action': 'run_e1_d2_customize', 'csrfmiddlewaretoken': $('#csrf_token').val(), 'classifier': classifier, 'actions': JSON.stringify(e1_d2_customize_options)},
        dataType: "json",
        success: function(response) {
            $('#e1_d2_customize_result_scores').text("Original: "+response.metrics[0][0]+"; Customized: "+response.metrics[0][1]);
            draw_e1_d2_customize_metrics(response.metrics);
            $('#e1_d2_customize_result').show('fast');
            $('#run_e1_d2_customize').val("Run");
            for(var key in e1_d2_customize_options){
                if(e1_d2_customize_options[key] != "remove"){
                    delete e1_d2_customize_options[key];
                }
            }
        },
        error: function(rs, e) {
            alert("Unexpected error. Please refresh the page and try again or contact me through email.");
            $('#run_e1_d2_customize').val("Run");
        }
    }); 
})

$(".process_options").change(function() {
    attribute_name = $(this).prev().text();
    if($(this).val() == "abstract"){
        if(statlog_continuous_attributes.includes(attribute_name)){
            new_div = $("#continuous_abstraction").clone(true).attr("id", attribute_name+"_abstraction").show();
            $("#"+attribute_name).append(new_div).show("fast");
        }
        else{
            new_div = $("#"+attribute_name+"_abstraction").clone(true).attr("id", attribute_name+"_abstraction_on").show();
            $("#"+attribute_name).append(new_div).show("fast");
        }
    }
    else if($(this).val() == "remove"){
        $("#"+attribute_name).hide("fast").find("div:last").remove();
        e1_d2_customize_options[attribute_name] = "remove";
    }
    else{
        $("#"+attribute_name).hide("fast").find("div:last").remove();
        if(attribute_name in e1_d2_customize_options){
            delete e1_d2_customize_options[attribute_name];
        }
    }
})

$(".continuous_abstraction_c1").change(function() {
    value = $(this).val();
    div_id = $(this).parent().parent().attr('id');
    $("#"+div_id+" .continuous_abstraction_cn").text(value);
})

$("#e1_d2_customize_control").click(function() {
    if($("#e1_d2_customize_control").val() == "Start" | $("#e1_d2_customize_control").val() == "Show"){
        $("#e1_d2_customize_content").show("fast");
        $("#e1_d2_customize_control").val("Hide");
    }
    else{
        $("#e1_d2_customize_content").hide("slow");
        $("#e1_d2_customize_control").val("Show");
    }
})

Chart.defaults.global.legend.display = false;
function draw_e1_d1_metrics(metrics) {
    draw_chart('e1_d1_result_sex_statistical_parity_difference', [metrics[1][0][0], metrics[1][0][1]], "Statistical parity difference", -1, 1);
    draw_chart('e1_d1_result_sex_equal_opportunity_difference', [metrics[1][1][0], metrics[1][1][1]], "Equal opportunity difference", -1, 1);
    draw_chart('e1_d1_result_sex_average_odds_difference', [metrics[1][2][0], metrics[1][2][1]], "Average odds difference", -1, 1);
    draw_chart('e1_d1_result_sex_disparate_impact', [metrics[1][3][0], metrics[1][3][1]], "Disparate impact", 0, 1);
    draw_chart('e1_d1_result_age_statistical_parity_difference', [metrics[2][0][0], metrics[2][0][1]], "Statistical parity difference", -1, 1);
    draw_chart('e1_d1_result_age_equal_opportunity_difference', [metrics[2][1][0], metrics[2][1][1]], "Equal opportunity difference", -1, 1);
    draw_chart('e1_d1_result_age_average_odds_difference', [metrics[2][2][0], metrics[2][2][1]], "Average odds difference", -1, 1);
    draw_chart('e1_d1_result_age_disparate_impact', [metrics[2][3][0], metrics[2][3][1]], "Disparate impact", 0, 1);
}

function draw_e1_d2_metrics(metrics) {
    draw_chart('e1_d2_result_sex_statistical_parity_difference', [metrics[1][0][0], metrics[1][0][1]], "Statistical parity difference", -1, 1);
    draw_chart('e1_d2_result_sex_equal_opportunity_difference', [metrics[1][1][0], metrics[1][1][1]], "Equal opportunity difference", -1, 1);
    draw_chart('e1_d2_result_sex_average_odds_difference', [metrics[1][2][0], metrics[1][2][1]], "Average odds difference", -1, 1);
    draw_chart('e1_d2_result_sex_disparate_impact', [metrics[1][3][0], metrics[1][3][1]], "Disparate impact", 0, 1);
    draw_chart('e1_d2_result_race_statistical_parity_difference', [metrics[2][0][0], metrics[2][0][1]], "Statistical parity difference", -1, 1);
    draw_chart('e1_d2_result_race_equal_opportunity_difference', [metrics[2][1][0], metrics[2][1][1]], "Equal opportunity difference", -1, 1);
    draw_chart('e1_d2_result_race_average_odds_difference', [metrics[2][2][0], metrics[2][2][1]], "Average odds difference", -1, 1);
    draw_chart('e1_d2_result_race_disparate_impact', [metrics[2][3][0], metrics[2][3][1]], "Disparate impact", 0, 1);
}

function draw_e1_d2_customize_metrics(metrics) {
    draw_chart('e1_d2_customize_result_sex_statistical_parity_difference', [metrics[1][0][0], metrics[1][0][1]], "Statistical parity difference", -1, 1);
    draw_chart('e1_d2_customize_result_sex_equal_opportunity_difference', [metrics[1][1][0], metrics[1][1][1]], "Equal opportunity difference", -1, 1);
    draw_chart('e1_d2_customize_result_sex_average_odds_difference', [metrics[1][2][0], metrics[1][2][1]], "Average odds difference", -1, 1);
    draw_chart('e1_d2_customize_result_sex_disparate_impact', [metrics[1][3][0], metrics[1][3][1]], "Disparate impact", 0, 1);
    draw_chart('e1_d2_customize_result_age_statistical_parity_difference', [metrics[2][0][0], metrics[2][0][1]], "Statistical parity difference", -1, 1);
    draw_chart('e1_d2_customize_result_age_equal_opportunity_difference', [metrics[2][1][0], metrics[2][1][1]], "Equal opportunity difference", -1, 1);
    draw_chart('e1_d2_customize_result_age_average_odds_difference', [metrics[2][2][0], metrics[2][2][1]], "Average odds difference", -1, 1);
    draw_chart('e1_d2_customize_result_age_disparate_impact', [metrics[2][3][0], metrics[2][3][1]], "Disparate impact", 0, 1);
}

function draw_e1_d2_improved_metrics(metrics) {
    draw_chart('e1_d2_improved_result_sex_statistical_parity_difference', [metrics[1][0][0], metrics[1][0][1]], "Statistical parity difference", -1, 1);
    draw_chart('e1_d2_improved_result_sex_equal_opportunity_difference', [metrics[1][1][0], metrics[1][1][1]], "Equal opportunity difference", -1, 1);
    draw_chart('e1_d2_improved_result_sex_average_odds_difference', [metrics[1][2][0], metrics[1][2][1]], "Average odds difference", -1, 1);
    draw_chart('e1_d2_improved_result_sex_disparate_impact', [metrics[1][3][0], metrics[1][3][1]], "Disparate impact", 0, 1);
    draw_chart('e1_d2_improved_result_age_statistical_parity_difference', [metrics[2][0][0], metrics[2][0][1]], "Statistical parity difference", -1, 1);
    draw_chart('e1_d2_improved_result_age_equal_opportunity_difference', [metrics[2][1][0], metrics[2][1][1]], "Equal opportunity difference", -1, 1);
    draw_chart('e1_d2_improved_result_age_average_odds_difference', [metrics[2][2][0], metrics[2][2][1]], "Average odds difference", -1, 1);
    draw_chart('e1_d2_improved_result_age_disparate_impact', [metrics[2][3][0], metrics[2][3][1]], "Disparate impact", 0, 1);
}

function draw_chart(element_id, data_list, title, suggestedMin, suggestedMax){
    backgroundColorOriginal = 'rgba(255, 99, 132, 0.2)';
    backgroundColorCustomized = 'rgba(54, 162, 235, 0.2)';
    borderColorOriginal = 'rgba(255, 99, 132, 1)';
    borderColorCustomized = 'rgba(54, 162, 235, 1)';
    var element = $('#'+element_id);
    var chart = new Chart(element, {
        type: 'bar',
        data: {
            labels: ['Original', 'Processed'],
            datasets: [{
                data: data_list,
                backgroundColor: [backgroundColorOriginal, backgroundColorCustomized],
                borderColor: [backgroundColorOriginal, backgroundColorCustomized],
                borderWidth: 1
            }]
        },
        options: {
            maintainAspectRatio: false,
            title: {display: true, text: title},
            scales: {yAxes: [{ticks: {suggestedMin: suggestedMin, suggestedMax: suggestedMax}}]},
        }
    });
}