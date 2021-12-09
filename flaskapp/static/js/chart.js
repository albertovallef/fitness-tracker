class Chart {
    constructor(config){
        this.data = config.data;
        this.start_date = config.start_date;
        this.end_date = config.end_date;
        this.element = config.element;
    }
    
    draw(){
        this.margin = {top: 10, right: 30, bottom: 60, left: 60},
        this.width = 1000 - this.margin.left - this.margin.right,
        this.height = 400 - this.margin.top - this.margin.bottom;

        var svg = d3.select(this.element)
        .append("svg")
        .attr("width", this.width + this.margin.left + this.margin.right)
        .attr("height", this.height + this.margin.top + this.margin.bottom);

        this.plot = svg.append("g")
            .attr("transform", "translate(" + this.margin.left + "," + this.margin.top + ")");

        this.createScales();
        this.addAxes();
        this.addLine();
    }

    createScales(){
        // Handling dates
        let min_date = new Date(this.start_date);
        let max_date = new Date(this.end_date);

        // Get datapoints
        function xValue(d) { return d.date; }      // accessors
        function yValue(d) { return d.weight; }

        // Create scales for x/y axis
        this.xScale = d3.scaleTime()
            .domain([min_date, max_date])
            .range([0, this.width]);

        console.log(d3.extent(this.data, yValue))

//        this.yScale = d3.scaleLinear()
//            .domain(d3.extent(this.data, yValue))
//            .range([this.height, 0]);
        this.yScale = d3.scaleLinear()
            .domain([d3.min(this.data,yValue) -10 , d3.max(this.data,yValue)+10])
            .range([this.height, 0]);
    }

    addAxes(){
        // Append the x/y axis
        this.plot.append("g")
        .attr("class", "x-axis")
        .attr("transform", "translate(0," + this.height + ")")
        .call(d3.axisBottom(this.xScale));

        this.plot.append("g")
            .attr("class", "y-axis")
            .call(d3.axisLeft(this.yScale));
    
        // Label axis
        // outer x-axis label
        this.plot.append("text")                         
            .attr("x", this.width/2)
            .attr("y", this.height + this.margin.bottom/3 + 10)
            .text("Date");
    
        // outer y-axis label
        this.plot.append("text")                         
            .attr("x", -this.height/2)
            .attr("y", -6 - this.margin.left/3)
            .attr("dy", "-.75em")
            .attr("transform", "rotate(-90)")
            .text("Weght(lb)");
    }

    addLine(){
        // Add the line
        let that = this;

        this.plot.append("path")
            .datum(this.data)
            .attr("fill", "none")
            .attr("class", "line")
            .attr("stroke", "#69b3a2")
            .attr("stroke-width", 1.5)
            .attr("d", d3.line()
            .x(function(d) { return that.xScale(new Date(d.date)); })
            .y(function(d) { return that.yScale(d.weight); })
            )

        this.plot
            .append("g")
            .attr("class", "datapoints")
                .selectAll("dot")
                .data(this.data)
                .enter()
                .append("circle")
                    .attr("cx", function(d) { return that.xScale(new Date(d.date)); })
                    .attr("cy", function(d) { return that.yScale(d.weight); })
                    .attr("r", 5)
                    .attr("fill", "#69b3a2")
    }

    updateChart(newData, start_date, end_date){
        this.data = newData;
        this.start_date = start_date;
        this.end_date = end_date;

        this.plot.selectAll(".line").remove();
        this.plot.selectAll(".datapoints").remove();
        this.plot.selectAll(".x-axis").remove();
        this.plot.selectAll(".y-axis").remove();

        this.createScales();
        this.addAxes();
        this.addLine();

    }
}