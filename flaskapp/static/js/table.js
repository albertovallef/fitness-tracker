class Table {
    constructor(config){
        this.data = config.data;
        this.columns = config.columns;
        this.element = config.element;
        this.table = d3.select(this.element).append("table");
    }

    draw(){
        this.thead = this.table.append("thead");
        this.tbody = this.table.append("tbody");
        this.add_rows();
    }

    add_rows() {
        let that = this;

        this.thead.append("tr")
            .selectAll("th").data(this.columns).enter()
                .append("th").text( function(column) { return column; });

        let rows = this.tbody.selectAll("tr")
            .data(this.data)
            .enter()
            .append("tr");

        let cells = rows.selectAll("td")
            .data(function (row) {
                return that.columns.map(function (column) {
                    return {column: column, value: row[column]};
                });
            })
            .enter().append("td")
                .text(function (d) { return d.value; })
    }

    delete_rows() {
        this.table.selectAll("thead").remove();
        this.table.selectAll("tbody").remove();
    }

    update_table(data, columns) {
        this.data = data;
        this.columns = columns;
        this.delete_rows();
        this.draw();
    }
}