/* Handle the search button click */

function backtest() {  
    // base_url = "http://ec2-100-20-59-199.us-west-2.compute.amazonaws.com:8888/backtest?stock_ticker=";
    base_url = "/backtest?stock_ticker=";
    
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
                var metrics = ["# Trades", "Return [%]", "Return (Ann.) [%]", "Exposure Time [%]",
			"Volatility (Ann.) [%]", "Max. Drawdown [%]", "Avg. Drawdown [%]",
			"Sharpe Ratio", "Sortino Ratio", "Calmar Ratio"];

                // Create table and set up the headers
                var table_body =  populate_header();

                // Append rows for indicators
                populate_signal(table_body, data, metrics, "MacdSignal", "MACD Signal");  
                populate_signal(table_body, data, metrics, "RsiSignal", "RSI Signal"); 
                populate_signal(table_body, data, metrics, "SmaCross", "SMA Cross"); 
                populate_signal(table_body, data, metrics, "StochOsci", "Stochastic Oscillator"); 
                populate_signal(table_body, data, metrics, "StochRsi", "Stochastic RSI"); 
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

    thead_tr.append("th").attr("class", 'table_header_cell').text("Strategy");
    thead_tr.append("th").attr("class", 'table_header_cell').text("Parameters");
    thead_tr.append("th").attr("class", 'table_header_cell').text("Metric");
    thead_tr.append("th").attr("class", 'table_header_cell').text("6-Month");

    thead_tr.append("th").attr("class", 'table_header_cell').text("1-Year");
    thead_tr.append("th").attr("class", 'table_header_cell').text("2-Year");
    thead_tr.append("th").attr("class", 'table_header_cell').text("CY2016");
    thead_tr.append("th").attr("class", 'table_header_cell').text("CY2017");

    thead_tr.append("th").attr("class", 'table_header_cell').text("CY2018");
    thead_tr.append("th").attr("class", 'table_header_cell').text("CY2019");
    thead_tr.append("th").attr("class", 'table_header_cell').text("CY2020"); 
    thead_tr.append("th").attr("class", 'table_header_cell').text("Details"); 
    
    // Return the table body to append rows.
    var tbody = table.append("tbody");
    return tbody;
} 

function populate_signal(tbody,  // table body to append rows
                         data,   // data
                         metrics,  // metrics to show
                         strategy_keyname,
                         strategy_displayname) {   
    
    var keys = [strategy_keyname.concat("_0.5"), strategy_keyname.concat("_1"), strategy_keyname.concat("_2"),
                strategy_keyname.concat("_2016"), strategy_keyname.concat("_2017"), strategy_keyname.concat("_2018"),
                strategy_keyname.concat("_2019"), strategy_keyname.concat("_2020")]; 


    ticker = document.getElementById("ticker").value;
    cash = document.getElementById("cash").value;
    commission = document.getElementById("commission").value;

    for (var i = 0; i < metrics.length; i++) {
        // Append one row for each metric
        var tbody_tr = tbody.append("tr");
        var cur_metric = metrics[i]; 

        // Add Strategy, Parameters, just one row for each strategy.
        if (i == 0) {
          tbody_tr.append("th").attr("rowspan", metrics.length).attr("class", 'table_cell').text(strategy_displayname);
          tbody_tr.append("th").attr("rowspan", metrics.length).attr("class", 'table_cell').text("Parameters");
        }

        // Current metric
        tbody_tr.append("th").attr("class", 'table_cell').text(cur_metric);

        // Loop over all keys for columns of metric values (6 month, 1 year, 2 year, CY2016~2020)
        for (var j = 0; j < keys.length; j++) {
            var strategy_with_date = keys[j];
            var metric_value = data[strategy_with_date][cur_metric];
            if (metric_value === null) {
                console.log("Metric is null: ".concat(metric_value))
                metric_value = "N/A"
            } else { 
                metric_value = metric_value.toPrecision(4)
            }
            tbody_tr.append("td").attr("class", 'table_cell').text(metric_value);
        }

        // Add details column
        if (i == 0) {
	  detail_page_url = "/backtest_details?stock_ticker=";
          detail_page_url = detail_page_url.concat(ticker);
          detail_page_url = detail_page_url.concat("&cash=");
          detail_page_url = detail_page_url.concat(cash);
          detail_page_url = detail_page_url.concat("&commission=");
          detail_page_url = detail_page_url.concat(commission);
          detail_page_url = detail_page_url.concat("&strategy=");
          detail_page_url = detail_page_url.concat(strategy_keyname);
          var cell_text = "<a href=";
	  cell_text = cell_text.concat(detail_page_url);
          cell_text = cell_text.concat(" target=_blank>Details</a>");
	  console.log(cell_text);
          tbody_tr.append("td").attr("rowspan", metrics.length)
			.attr("class", 'table_cell').html(cell_text);
	}
    }  
}  




