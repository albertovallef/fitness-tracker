$( document ).ready( () => {
    $("#start_workout").click( () => {
        $('.workout-tab').css('visibility',"visible");
    })
    $(".close-button").click( () => {
        $('.workout-tab').css('visibility',"hidden");
    })
});