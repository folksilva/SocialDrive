/**
 * 
 */
var reg = new RegExp('^[A-z]{3}-[0-9]{4}$');

$(document).ready(function(){
	$(".modal").hide();
	$("#plate").mask("aaa-9999");
	$("#plate").keyup(function(){
		if(reg.test($(this).val())){
			$("#msg").focus();
		}
	});
	$("#msg").keyup(function(){
		if($(this).val().length > 200){
			$(this).val($(this).val().substring(0,200));
		}
		$("#msg-counter").html(200-$(this).val().length);
	});
	$("#t").keyup(function(){
		if($(this).val().length > 200){
			$(this).val($(this).val().substring(0,200));
		}
		$("#reply-counter").html(200-$(this).val().length);
	});
	$("#socialdrive").submit(function(){
		$("#flash").html("");
		var plate = $("#plate").val();
		if(!reg.test(plate)){
			$("#plate").val("ABC-1234");
			$("#plate").focus();
			$("#flash").html("Com essa placa não dá. =(");
			return false
		}else if(!$("#msg").val().length>0){
			$("#msg").focus();
			$("#flash").html("Ei, faltou a mensagem!");
			return false
		}
		return true;
	})
	$("#reply-message").submit(function(){
		$("#flash").html("");
		if(!$("#t").val().length>0){
			$("#t").focus();
			return false
		}
		return true;
	})
});

function showMessages(){
	$("#flash").html("")
	var plate = $("#plate").val();
	if(reg.test(plate)){
		window.location = "?p="+plate.toUpperCase();
	}else{
		$("#plate").val("ABC-1234");
		$("#plate").focus();
		$("#flash").html("Com essa placa não dá. =(");
	}
}

function reply(msg){
	$("#m").val(msg);
	$("#t").val("");
	$(".modal").fadeIn();
}

function undoReply(){
	$("#m").val("");
	$(".modal").fadeOut();
}
