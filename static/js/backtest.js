/* Handle the search button click */
function backtest() {
    console.log();
    base_url = "/backtest?stock_ticker=";
    ticker = document.getElementById("ticker").value;
    data_url = base_url.concat(ticker);

    console.log(ticker);
    console.log(data_url);
    
    /* https://bl.ocks.org/d3noob/473f0cf66196a008cf99 */
    d3.json(data_url.concat("&cash=10000&commission=0"),
            function(err, data) {
                if (err) throw err;
                console.log(data);


                document.getElementById("indicator_table").innerHTML = JSON.stringify(data);
                

		// Create the table.
		/*
		var table = d3.select("#indicator_table").append("table")
            			.attr("style", "margin-left: 250px");
                var thead = table.append("thead");
                var tbody = table.append("tbody");    
		*/

	        // Create the header row.
		/*
                thead.append("tr")
                     .selectAll("th")
                     .data(columns)
                     .enter()
                     .append("th")
                        .text(function(column) { return column; });
			*/
            }
    );
}
