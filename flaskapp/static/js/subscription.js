$( document ).ready( () => {

});

function subscribe(trainer){
    console.log(trainer);

    $.ajax({
        url: 'subscribe',
        contentType: 'application/json',
        dataType: 'json',
        type: 'POST',
        data: JSON.stringify(trainer),
        success: function (response) {
            console.log(response)
            updateTables(response)

        },
        error: function (response) {
            console.log(response)
        }
    });
}

function unsubscribe(trainer){
    console.log(trainer);

    $.ajax({
        url: 'unsubscribe',
        contentType: 'application/json',
        dataType: 'json',
        type: 'POST',
        data: JSON.stringify(trainer),
        success: function (response) {
            console.log(response)
            updateTables(response)

        },
        error: function (response) {
            console.log(response)
        }
    });
}

function updateTables(response){
    console.log(response)
}