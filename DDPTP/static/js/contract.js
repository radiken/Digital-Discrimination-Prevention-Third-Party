$("#add_field").click(function() {
    $("#new_field").clone(true).insertBefore(this).attr("id", "").show('fast');
});

$(".remove").click(function() {
    $target = $(this).parent();
    $target.hide('slow', function(){ $target.remove(); });
});

$(".field_type").change(function(){
    if($(this).val()=="choice_field"){
        $(this).next().hide('fast');
        $(this).next().next().show('fast');
    }
    if($(this).val()=="text_field"){
        $(this).next().show('fast');
        $(this).next().next().hide('fast');
    }
});

$(".add_choice").click(function() {
    $("#new_choice").clone(true).insertBefore($(this)).attr("id", "").show('fast');
});

$(function() {
    $(".is_sensitive").change(function()
    {
    if ($(this).is(':checked')){
        $(this).next().show('fast');
    }
    else{
        $(this).next().hide('fast');
    }
    });
});

$(".sensitive_type").change(function(){
    if($(this).val()=="hide"){
        $(this).next().hide('fast');
    }
    if($(this).val()=="abstract"){
        $(this).next().show('fast');
    }
});

$("#submission").click(function() {
    if($('.field').length <= 1){
        alert("You have to create at least one field!");
        $("#form").attr("action", "");
    }
});