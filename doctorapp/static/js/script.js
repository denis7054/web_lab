
$("figure img").hover(
    function() {
        $(this).animate({
            width: "550px",
            height: "550px",
            borderRadius: "2%"
        }, "slow");

    }, function() {
        $(this).animate({
        width: "500px",
        height: "500px",
        borderRadius: "10%"
    }, "slow");
    });

    
// function toggleText(){
//     var hiddenText = document.getElementById("hiddenText");
//     if(hiddenText.style.maxHeight == "0px"){
//         hiddenText.style.maxHeight = hiddenText.scrollHeight + "px";
//     }
//     else{
//         hiddenText.style.maxHeight = "0px";
//     }
// }


$(document).ready(function() {
	$(".hidebox p").hide();
	// $(".hidebox h3").css("background-color", "#29c5e6");
});
$(".hidebox h3").click(function () {
	$(this).next("p").hide("slow");
	// $(this).css("background-color", "#008000");
	// $(this).css("color", "#fff");

});
$(".hidebox h3").dblclick(function () {
	$(this).next("p").show("slow");
	// $(this).css("background-color", "#E4DC23");
	// $(this).css("color", "#000000");

});
    