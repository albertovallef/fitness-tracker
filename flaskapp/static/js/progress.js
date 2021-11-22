// Calendar settings
$( function() {
    $( "#start-date" ).datepicker({
        dateFormat: "yy-mm-dd"
    });
    $( "#end-date" ).datepicker({
        dateFormat: "yy-mm-dd"
    });
  } );


  $( document ).ready(() => {
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
                create_chart(response, start_date, end_date)
            },
            error: function (response) {
                console.log(response)
            }
        });
    })

  })

  function create_chart(data, star_date, end_date) {
    
    // setting up the chart dimensions
    var margin = {top: 10, right: 30, bottom: 60, left: 60},
    width = 1000 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    var svg = d3.select("#chart")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

    // Handling dates
    min_date = new Date(star_date);
    max_date = new Date(end_date);

    // Get datapoints
    function xValue(d) { return d.date; }      // accessors
    function yValue(d) { return d.weight; }

    // Create scales for x/y axis
    var xScale = d3.scaleTime()
        .domain([min_date, max_date])
        .range([0, width]);
    
    var yScale = d3.scaleLinear()
        .domain(d3.extent(data, yValue))
        .range([height, 0]);

    // Append the x/y axis
    svg.append("g")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(xScale));

    svg.append("g")
      .call(d3.axisLeft(yScale));
    
    // Label axis
    // outer x-axis label
    svg.append("text")                         
    .attr("x", width/2)
    .attr("y", height + margin.bottom/3 + 10)
    .text("Date");
    
    // outer y-axis label
    svg.append("text")                         
    .attr("x", -height/2)
    .attr("y", -6 - margin.left/3)
    .attr("dy", "-.75em")
    .attr("transform", "rotate(-90)")
    .text("Weght(lb)");

    // Add the line
    svg.append("path")
    .datum(data)
    .attr("fill", "none")
    .attr("stroke", "#69b3a2")
    .attr("stroke-width", 1.5)
    .attr("d", d3.line()
      .x(function(d) { return xScale(new Date(d.date)); })
      .y(function(d) { return yScale(d.weight); })
      )

    // Add the points
    svg
      .append("g")
      .selectAll("dot")
      .data(data)
      .enter()
      .append("circle")
        .attr("cx", function(d) { return xScale(new Date(d.date)); })
        .attr("cy", function(d) { return yScale(d.weight); })
        .attr("r", 5)
        .attr("fill", "#69b3a2")
  }
