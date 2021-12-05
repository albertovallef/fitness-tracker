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
    var trainerTable = document.getElementById("trainers");
    var subTable = document.getElementById("subs");
    trainerTable.innerHTML = '<tr> <th>Trainers</th> <th class=trainer-subscribe>Subscribe</th> </tr>'
    subTable.innerHTML = "<tr><th>Subscribtions</th><th class=trainer-subscribe>Unsubscribe</th></tr>"
    
    var trainers = response[0]
    var subs = response[1]


    for(var i = 0; i < subs.length; i++){
        var tr = document.createElement("tr");
        var trainer = document.createElement('td')
        trainer.innerHTML='&nbsp;' + subs[i]
        
        var buttontd = document.createElement('td')
        var button = document.createElement("button");
        button.setAttribute('id', subs[i])
        button.setAttribute('value', "submit")
        button.setAttribute('class', "btn unsub-button")
        button.setAttribute('onclick', "unsubscribe(this.id)")
        button.innerHTML = "Unsubscribe"

        buttontd.appendChild(button)

        tr.appendChild(trainer)
        tr.appendChild(button)
        subTable.appendChild(tr)
    }

    for(var i = 0; i < trainers.length; i++){
        var tr = document.createElement("tr");
        var trainer = document.createElement('td')
        trainer.innerHTML='&nbsp;' + trainers[i]
        
        var buttontd = document.createElement('td')
        var button = document.createElement("button")
        button.setAttribute('id', trainers[i])
        button.setAttribute('value', "submit")
        button.setAttribute('class', "btn sub-button default")
        button.setAttribute('onclick', "subscribe(this.id)")
        button.innerHTML = "Subscribe"

        buttontd.appendChild(button)
        tr.appendChild(trainer)
        tr.appendChild(buttontd)
        trainerTable.appendChild(tr)
    }
    // for(var i = 0; i < response[1].length; i++){
    //     var option = document.createElement("option");
    //     option.setAttribute('id','option-exe')
    //     var text = document.createTextNode(exercises[i])
    //     option.appendChild(text)
    //     old.appendChild(option)
    // }
}