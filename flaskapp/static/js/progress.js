// Calendar settings
$( function() {
    $( "#start-date" ).datepicker({
        dateFormat: "yy-mm-dd"
    });
    $( "#end-date" ).datepicker({
        dateFormat: "yy-mm-dd"
    });
  });


  $( document ).ready(() => {

    var current_date = new Date; // get current date
    var first = current_date.getDate() - current_date.getDay(); // First day is the day of the month - the day of the week
    var last = first + 6; // last day is the first day + 6

    var start_date = new Date(current_date.setDate(first)).toISOString().split('T')[0];
    var end_date = new Date(current_date.setDate(last)).toISOString().split('T')[0];
    exe_name = document.getElementById("select-exercise").value;

    var client_data = {
      "exercise": exe_name,
      "start_date": start_date,
      "end_date": end_date,
      };
    
    var datapoints = $.ajax({
      url: 'view_progress',
      contentType: 'application/json',
      dataType: 'json',
      type: 'POST',
      async: false,
      data: JSON.stringify(client_data)}).responseJSON;

    var chart = new Chart({
      element: document.getElementById("chart"),
      data: datapoints,
      start_date: client_data["start_date"],
      end_date: client_data["end_date"]
    })
    
    $("#view-progress-btn").click( () => {
        exe_name = document.getElementById("select-exercise").value;
        start_date = document.getElementById("start-date").value;
        end_date = document.getElementById("end-date").value;

        var client_data = {
            "exercise": exe_name,
            "start_date": start_date,
            "end_date": end_date,
          };
        
        $.ajax({
          url: 'view_progress',
          contentType: 'application/json',
          dataType: 'json',
          type: 'POST',
          data: JSON.stringify(client_data),
          success: function (response) {
            chart.updateChart(response, start_date, end_date)
          },
          error: function (response) {
              console.log(response)
          }
        });
    })
  })