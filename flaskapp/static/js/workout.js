$( document ).ready( () => {
    $("#start_workout").click( () => {
        $('.workout-tab').css('visibility',"visible");
    })
    $(".close-button").click( () => {
        $('.workout-tab').css('visibility',"hidden");
    })
    $("#add-set").click( () => {
        var content_table = document.getElementById("workout-tab-content");
        var add_exercise_eleme = document.getElementById("add-exercise");
        var cloned_elem = add_exercise_eleme.cloneNode(true);
        content_table.appendChild(cloned_elem);
    })
});