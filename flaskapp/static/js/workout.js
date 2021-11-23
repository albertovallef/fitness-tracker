// set global variables
var id = 0;

$( document ).ready( () => {
    $("#start_workout").click( () => {
        $('.workout-tab').css('visibility',"visible");
        $.ajax({
            url: 'training_session',
            contentType: 'application/json',
            dataType: 'json',
            type: 'POST',
            data: JSON.stringify("New session"),
            success: function (response) {
                $('#start_workout_span').text(response);
            },
            error: function (response) {
                $('#start_workout_span').text("An error has occurred, please try again :(");
                console.log(response)
            }
        });
    })
    $(".close-button").click( () => {
        $('.workout-tab').css('visibility',"hidden");
        $('.workout-inputs').css('visibility',"hidden");
    })
    $("#add-set").click( () => {
        $('.workout-inputs').css('visibility',"visible");
        id += 1;
        var content_table = document.getElementById("workout-tab-content");
        var table = createTable(id);
        content_table.appendChild(table);

    })
    $("#add-exercise-btn").click( () => {
        var table = document.getElementById("table" + id);
        exe_name = document.getElementById("select-exercise").value;
        reps = document.getElementById("input-reps").value;
        weight = document.getElementById("input-weight").value;
        duration = document.getElementById("input-duration").value;
        data = [exe_name, reps, weight, duration];
        var row = createExerciseRow(data);
        table.appendChild(row);
        var client_data = {
            "exercise": data[0],
            "reps": data[1],
            "weight": data[2],
            "duration": data[3]
            };
            
        $.ajax({
            url: 'add_workout',
            contentType: 'application/json',
            dataType: 'json',
            type: 'POST',
            data: JSON.stringify(client_data),
            success: function (response) {
                console.log(response)
            },
            error: function (response) {
                console.log(response)
            }
        });
    })
});

function createTable(id) {
    var table = document.createElement("table");
    var columns = ["Exercise Name", "Reps", "Weight", "Duration"];
    var tr = document.createElement("tr");
    for(var i = 0; i < columns.length; i++){
        var th = document.createElement("th");
        var text = document.createTextNode(columns[i]);
        th.appendChild(text);
        tr.appendChild(th);
    }
    table.appendChild(tr);
    table.setAttribute("id", "table" + id);

    return table;
}

function createExerciseRow(data){
    var tr = document.createElement("tr");
    for(var i = 0; i < data.length; i++){
        var td = document.createElement("td");
        var text = document.createTextNode(data[i]);
        td.appendChild(text);
        tr.appendChild(td);
    }
    return tr;
}