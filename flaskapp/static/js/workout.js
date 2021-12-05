// set global variables
var id = 0;

$( document ).ready( () => {
    $("#start_workout").click( () => {
        $('.workout-tab').css('visibility',"visible");
        addSep()
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

    $("#new-seperator").click( () => {
        // $('.workout-inputs').css('visibility',"visible");
        addSep()
    })

    $("#add-set").click( () => {
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

    $("#reset-filter").click( () => {
        console.log("RESETTING FILTER")
        $.ajax({
            url: 'get-exercises',
            contentType: 'application/json',
            dataType: 'json',
            type: 'POST',
            success: function (response) {
                console.log(response)
                updateExercises(response)
            },
            error: function (response) {
                console.log(response)
            }
        });
    })


    $("#search-by-cat").click( () => {
        category = document.getElementById("by_cat").value;
        $.ajax({
            url: 'search-by-cat',
            contentType: 'application/json',
            dataType: 'json',
            type: 'POST',
            data: JSON.stringify(category),
            success: function (response) {
                console.log(response)
                updateExercises(response)
            },
            error: function (response) {
                console.log(response)
            }
        });
    })
});


function updateExercises(exercises) {
    var old = document.getElementById("select-exercise");
    old.innerHTML='';
    for(var i = 0; i < exercises.length; i++){
        var option = document.createElement("option");
        option.setAttribute('id','option-exe')
        var text = document.createTextNode(exercises[i])
        option.appendChild(text)
        old.appendChild(option)
    }
}

function addSep() {
    id += 1;
    var content_table = document.getElementById("workout-tab-content");
    var table = createTable(id);
    content_table.appendChild(table);
}

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