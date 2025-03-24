$(document).ready(function () {
    console.log("Testing");
    $(window).scroll(function () {
        if($(document).scrollTop() > 50){
            $(".card shadow-sm bg-dark text-white").css("text-white", "black")
        }else{
            $(".card shadow-sm bg-dark text-white").css("text-white", "white")
        }
    })
    //
    // let card = document.getElementsByClassName("card");
    // $(card).hover(function () {
    //     $(card).css("visibility", "visible");
    //     // alert("Hovered over Card")
    // }, function () {
    //     $(card).css("visiblity", "hidden");
    // });
})

