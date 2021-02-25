/* Handle the search button click */

function backtest() {  
    base_url = "http://ec2-100-20-59-199.us-west-2.compute.amazonaws.com:8888/backtest?stock_ticker=";
    
    ticker = document.getElementById("ticker").value;
    cash = document.getElementById("cash").value;
    commission = document.getElementById("commission").value;
    
    data_url = base_url.concat(ticker)
                .concat("&cash=").concat(cash)
                .concat("&commission=").concat(commission);

    console.log(ticker);
    console.log(cash);
    console.log(commission); 
    console.log(data_url); 

    // https://bl.ocks.org/d3noob/473f0cf66196a008cf99 
    d3.json(data_url,
            function(err, data) {
                if (err) throw err;
                console.log(data);

                // document.getElementById("indicator_table").innerHTML = JSON.stringify(data); 
                
                // Metrics we care about.
                var metrics = ["Return [%]", "Return (Ann.) [%]", "Exposure Time [%]", "Volatility (Ann.) [%]",
                               "Max. Drawdown [%]", "Avg. Drawdown [%]", "Sharpe Ratio", "Sortino Ratio", 
                               "Calmar Ratio"];

                // Create table and set up the headers
                var table_body =  populate_header();

                // Append rows for MACD
                populate_MacdSignal(table_body, data, metrics);
            }
    );
} 

function populate_header() { 
    // Clear existing items
    d3.select("#indicator_table").html("");

    // Now, add table.
    var table = d3.select("#indicator_table").append("table").attr("width", 1150);
    var thead = table.append("thead");
    var thead_tr = thead.append("tr");
    thead_tr.append("th").attr("width", "11%").attr("class", 'table_header_cell').text("Strategy");
    thead_tr.append("th").attr("width", "10%").attr("class", 'table_header_cell').text("Parameters");
    thead_tr.append("th").attr("width", "23%").attr("class", 'table_header_cell').text("Metric");
    thead_tr.append("th").attr("width", "8%").attr("class", 'table_header_cell').text("6-Month");

    thead_tr.append("th").attr("width", "6%").attr("class", 'table_header_cell').text("1-Year");
    thead_tr.append("th").attr("width", "6%").attr("class", 'table_header_cell').text("2-Year");
    thead_tr.append("th").attr("width", "6%").attr("class", 'table_header_cell').text("CY2016");
    thead_tr.append("th").attr("width", "6%").attr("class", 'table_header_cell').text("CY2017");

    thead_tr.append("th").attr("width", "6%").attr("class", 'table_header_cell').text("CY2018");
    thead_tr.append("th").attr("width", "6%").attr("class", 'table_header_cell').text("CY2019");
    thead_tr.append("th").attr("width", "6%").attr("class", 'table_header_cell').text("CY2020"); 
    thead_tr.append("th").attr("width", "6%").attr("class", 'table_header_cell').text("Details");
    
    // Return the table body to append rows.
    var tbody = table.append("tbody");
    return tbody;
} 

function populate_MacdSignal(tbody,  // table body to append rows
                             data,   // data 
                             metrics) {   
    
    var keys = ["MacdSignal_0.5", "MacdSignal_1", "MacdSignal_2",
                "MacdSignal_2016", "MacdSignal_2017", "MacdSignal_2018",
                "MacdSignal_2019", "MacdSignal_2020"];

    for (var i = 0; i < metrics.length; i++) {
        // Append one row for each metric
        var tbody_tr = tbody.append("tr");
        var cur_metric = metrics[i]; 

        // Add Strategy, Parameters, and Metrics column.
        tbody_tr.append("th").attr("class", 'table_cell').text("MACD");
        tbody_tr.append("th").attr("class", 'table_cell').text("Parameters");
        tbody_tr.append("th").attr("class", 'table_cell').text(cur_metric);

        // Loop over all keys for columns of metric values (6 month, 1 year, 2 year, CY2016~2020)
        for (var j = 0; j < keys.length; j++) {
            var strategy_with_date = keys[j];
            var metric_value = data[strategy_with_date][cur_metric];
            tbody_tr.append("th").attr("class", 'table_cell').text(metric_value);
        }

        // Add details column
        tbody_tr.append("th").attr("class", 'table_cell').text("Details");
    } 

    console.log(data['MacdSignal_0.5']) 

} 


