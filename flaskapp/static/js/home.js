$( document ).ready( () => {

});

function updateBody(stat){
    console.log(stat)

    var value = document.getElementById(stat+'-val').value

    //makes sure user put a value in
    if(value == ''){
        alert('Text field is empty!')
        return
    }

    $.ajax({
        url: 'update-body',
        contentType: 'application/json',
        dataType: 'json',
        type: 'POST',
        data: JSON.stringify(['b_'+ stat,value]),
        success: function (response) {
            console.log(response)

            //update td
            var text = stat.charAt(0).toUpperCase() + stat.slice(1) + ': ' +  value
            if(stat == 'height'){
                text += ' inches'
            }else if(stat == 'weight'){
                text += ' lbs'
            }
            document.getElementById(stat+'-text').innerHTML = text
        },
        error: function (response) {
            console.log(response)
        }
    });
}

function updateGender(gender){
    console.log(gender)
    if(gender == 'Male'){
        text = 'female'
    }else {
        text = 'male'
    }

    document.getElementById('gender-button').setAttribute('class', 'btn btn-primary ' + text)
    document.getElementById('gender-button').innerHTML = text.charAt(0).toUpperCase() + text.slice(1)
    // document.getElementById('gender-text').innerHTML = 'Gender: ' + text.charAt(0).toUpperCase() + text.slice(1)

    $.ajax({
        url: 'update-body',
        contentType: 'application/json',
        dataType: 'json',
        type: 'POST',
        data: JSON.stringify(['b_gender', text]),
        success: function (response) {
            console.log(response)

        },
        error: function (response) {
            console.log(response)
        }
    });
}
