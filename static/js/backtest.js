/* Handle the search button click */

function backtest() {  
    // base_url = "http://ec2-100-20-59-199.us-west-2.compute.amazonaws.com:8888/backtest?stock_ticker=";
    base_url = "/backtest?stock_ticker=";
            
    ticker = document.getElementById("ticker").value;
    data_url = base_url.concat(ticker);

    console.log(ticker);
    console.log(data_url); 

    // https://bl.ocks.org/d3noob/473f0cf66196a008cf99 
    d3.json(data_url,
            function(err, data) {
                if (err) throw err;
                console.log(data);

		if ('err_msg' in data) {
                  var err_msg = "<p style='color:red;font-size:25px;font-family:courier;'>"
                                        .concat(data.err_msg)
                                        .concat("</p>");
                  d3.select("#indicator_table").html(err_msg);
                  return;
		}

                // document.getElementById("indicator_table").innerHTML = JSON.stringify(data); 
                
                // Metrics we care about.
                var metrics = ["Return [%]", "Return (Ann.) [%]", "Exposure Time [%]", "Win Rate [%]", "# Trades",
			"Volatility (Ann.) [%]", "Max. Drawdown [%]", "Avg. Drawdown [%]",
			"Sharpe Ratio", "Sortino Ratio", "Calmar Ratio"];

                // Create table and set up the headers
                var table_body =  populate_header();

                // Append rows for indicators
                populate_signal(table_body, data, metrics, "BuyAndHold", "Buy and Hold", "table_cell_0");  
                add_table_separator(table_body);

                insert_header_row(table_body);
                populate_signal(table_body, data, metrics, "SmaCross", "SMA Cross", "table_cell_1"); 
                add_table_separator(table_body);

                insert_header_row(table_body);
                populate_signal(table_body, data, metrics, "MacdSignal", "MACD Signal", "table_cell_0");  
                add_table_separator(table_body);

                insert_header_row(table_body);
                populate_signal(table_body, data, metrics, "StochOsci", "Stochastic Oscillator", "table_cell_1"); 
                add_table_separator(table_body);

                insert_header_row(table_body);
                populate_signal(table_body, data, metrics, "StochRsi", "Stochastic RSI", "table_cell_0"); 
                add_table_separator(table_body);

                insert_header_row(table_body);
                populate_signal(table_body, data, metrics, "ARIMA_Pred", "ARIMA Time Series", "table_cell_1"); 
                add_table_separator(table_body);

                insert_header_row(table_body);
                populate_signal(table_body, data, metrics, "LogReg_Signal", "Logistic Regression", "table_cell_0"); 

                //populate_signal(table_body, data, metrics, "RsiSignal", "RSI Signal"); 
                // Append footnote
                
                var foot_note = "[1] Only the following tickers are supported for strategy of Arima_Pred and LogReg_Signal: "
                                .concat("SPY, QQQ, EEM, AAPL, MSFT, TSLA, GOOG, GOOGL");
                d3.select("#indicator_table").append("p")
                        .style("padding", "10px")
                        .style("font-size", "10px")
                        .style("font-family", "courier").text(foot_note);
            }
    );
} 

function populate_header() { 
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

    thead_tr.append("th").attr("class", 'table_header_cell').text("CY2020"); 
    thead_tr.append("th").attr("class", 'table_header_cell').text("CY2019");
    thead_tr.append("th").attr("class", 'table_header_cell').text("CY2018");
    thead_tr.append("th").attr("class", 'table_header_cell').text("CY2017");
    thead_tr.append("th").attr("class", 'table_header_cell').text("CY2016");
    thead_tr.append("th").attr("class", 'table_header_cell').text("Details"); 
    
    // Return the table body to append rows.
    var tbody = table.append("tbody");
    return tbody;
} 

// This is similar to the func above, just that it will not create table header. Instead,
// it inserts another row with similar style with the header.
function insert_header_row(tbody) { 
    var tbody_tr = tbody.append("tr");
    tbody_tr.append("td").attr("class", 'table_header_cell').text("Strategy");
    tbody_tr.append("td").attr("class", 'table_header_cell').text("Parameters");
    tbody_tr.append("td").attr("class", 'table_header_cell').text("Metric");

    tbody_tr.append("td").attr("class", 'table_header_cell').text("6-Montd");
    tbody_tr.append("td").attr("class", 'table_header_cell').text("1-Year");
    tbody_tr.append("td").attr("class", 'table_header_cell').text("2-Year");

    tbody_tr.append("td").attr("class", 'table_header_cell').text("CY2020"); 
    tbody_tr.append("td").attr("class", 'table_header_cell').text("CY2019");
    tbody_tr.append("td").attr("class", 'table_header_cell').text("CY2018");
    tbody_tr.append("td").attr("class", 'table_header_cell').text("CY2017");
    tbody_tr.append("td").attr("class", 'table_header_cell').text("CY2016");
    tbody_tr.append("td").attr("class", 'table_header_cell').text("Details"); 
    return ;
}

function add_table_separator(tbody) {
  var tbody_tr = tbody.append("tr");
  var sep = "----------------------------------------------------------------------------------";
  sep = sep.concat(sep).concat(sep);
  tbody_tr.append("td").attr("colspan", "12").attr("class", "table_separator").text(sep);
}

function populate_signal(tbody,  // table body to append rows
                         data,   // data
                         metrics,  // metrics to show
                         strategy_keyname,
                         strategy_displayname,
                         cell_class) {   // CSS style class for table cell 
    
    var keys = [strategy_keyname.concat("_0.5"), strategy_keyname.concat("_1"), strategy_keyname.concat("_2"),
                strategy_keyname.concat("_2020"), strategy_keyname.concat("_2019"), strategy_keyname.concat("_2018"),
                strategy_keyname.concat("_2017"), strategy_keyname.concat("_2016")]; 

    var parameters_map = {
	    "BuyAndHold": "",
	    "SmaCross": `<div style="text-align:center">
	                    Short SMA <br> <input type='text' id='sma_short_sma' value='3' style='background-color:#e8e8e8;' size='18%' readonly>  <br>
	                    Long SMA <br> <input type='text' id='sma_long_sma' value='15' style='background-color:#e8e8e8;' size='18%' readonly> <br>
	                    Long Only <br> <input type='text' id='sma_long_only' value='Yes' style='background-color:#e8e8e8;' size='18%' readonly>
	                 </div>`,
	    "MacdSignal": `<div style="text-align:center">
	                    Fast Period <br> <input type='text' id='macd_fast_period' value='12' style='background-color:#e8e8e8;' size='18%' readonly>  <br>
	                    Slow Period <br> <input type='text' id='macd_slow_period' value='26' style='background-color:#e8e8e8;' size='18%' readonly> <br>
	                    Signal Period <br> <input type='text' id='macd_signal_period' value='9' style='background-color:#e8e8e8;' size='18%' readonly> <br>
	                    Long Only <br> <input type='text' id='macd_long_only' value='Yes' style='background-color:#e8e8e8;' size='18%' readonly>
	                 </div>`,
	    "StochOsci": `<div style="text-align:center">
	                    Fast K Period <br> <input type='text' id='osci_fast_k_period' value='14' style='background-color:#e8e8e8;' size='18%' readonly>  <br>
	                    Slow K Period <br> <input type='text' id='osci_slow_k_period' value='3' style='background-color:#e8e8e8;' size='18%' readonly> <br>
	                    Slow D Period <br> <input type='text' id='osci_slow_d_period' value='3' style='background-color:#e8e8e8;' size='18%' readonly> <br>
	                    Overbought <br> <input type='text' id='osci_overbought' value='80' style='background-color:#e8e8e8;' size='18%' readonly> <br>
	                    Oversold <br> <input type='text' id='osci_oversold' value='20' style='background-color:#e8e8e8;' size='18%' readonly> <br>
	                    Long Only <br> <input type='text' id='osci_long_only' value='Yes' style='background-color:#e8e8e8;' size='18%' readonly>
	                 </div>`,
	    "StochRsi": `<div style="text-align:center">
	                    Time Period <br> <input type='text' id='rsi_time_period' value='14' style='background-color:#e8e8e8;' size='18%' readonly>  <br>
	                    Fast K Period <br> <input type='text' id='rsi_fast_k_period' value='14' style='background-color:#e8e8e8;' size='18%' readonly> <br>
	                    Fast D Period <br> <input type='text' id='rsi_fast_d_period' value='3' style='background-color:#e8e8e8;' size='18%' readonly> <br>
	                    Overbought <br> <input type='text' id='rsi_overbought' value='80' style='background-color:#e8e8e8;' size='18%' readonly> <br>
	                    Oversold <br> <input type='text' id='rsi_oversold' value='20' style='background-color:#e8e8e8;' size='18%' readonly> <br>
	                    Long Only <br> <input type='text' id='rsi_long_only' value='Yes' style='background-color:#e8e8e8;' size='18%' readonly>
	                 </div>`,
	    "ARIMA_Pred": `<div style="text-align:center">
	                    TODO <br> <input type='text' id='arima_1' value='3' style='background-color:#e8e8e8;' size='18%' readonly> <br>
	                    TODO <br> <input type='text' id='arima_2' value='80' style='background-color:#e8e8e8;' size='18%' readonly> <br>
	                    TODO <br> <input type='text' id='arima_3' value='20' style='background-color:#e8e8e8;' size='18%' readonly> <br>
	                    Long Only <br> <input type='text' id='arima_long_only' value='Yes' style='background-color:#e8e8e8;' size='18%' readonly>
	                 </div>`,
	    "LogReg_Signal": `<div style="text-align:center">
	                    Return metric <br> <input type='text' id='reg_metric' value='Next 5 day' style='background-color:#e8e8e8;' size='18%' readonly> <br>
	                    Buy threshold <br> <input type='text' id='reg_buy' value='1%' style='background-color:#e8e8e8;' size='18%' readonly> <br>
	                    Sell threshold <br> <input type='text' id='reg_sell' value='-1%' style='background-color:#e8e8e8;' size='18%' readonly> <br>
	                    Long Only <br> <input type='text' id='rsi_long_only' value='Yes' style='background-color:#e8e8e8;' size='18%' readonly>
	                 </div>`

    };



    ticker = document.getElementById("ticker").value;

    for (var i = 0; i < metrics.length; i++) {
        // Append one row for each metric
        var tbody_tr = tbody.append("tr");
        var cur_metric = metrics[i]; 

        // Add Strategy, Parameters, just one row for each strategy.
        if (i == 0) {
          if (strategy_keyname == 'ARIMA_Pred' || strategy_keyname == 'LogReg_Signal') {
             strategy_displayname = strategy_displayname
                        .concat('<sup>1</sup>');
          }
          tbody_tr.append("th").attr("rowspan", metrics.length).attr("class", cell_class).html(strategy_displayname);
          parameters_html = parameters_map[strategy_keyname];
          tbody_tr.append("th").attr("rowspan", metrics.length).attr("class", cell_class).html(parameters_html);
        }

        // Current metric
        tbody_tr.append("th").attr("class", cell_class).text(cur_metric);

        // Loop over all keys for columns of metric values (6 month, 1 year, 2 year, CY2016~2020)
        for (var j = 0; j < keys.length; j++) {
            var strategy_with_date = keys[j];
            var metric_value = null;
            if (strategy_with_date in data) {
                metric_value = data[strategy_with_date][cur_metric];
            }
            if (metric_value === null) {
                console.log("Metric is null: ".concat(metric_value))
                metric_value = "N/A"
            } else { 
                metric_value = metric_value.toPrecision(4)
            }
            tbody_tr.append("td").attr("class", cell_class).text(metric_value);
        }

        // Add details column
        if (i == 0) {
	  //detail_page_url = "/backtest_details?stock_ticker=";
	  detail_page_url = "/details?stock_ticker=";
          detail_page_url = detail_page_url.concat(ticker);
          detail_page_url = detail_page_url.concat("&strategy=");
          detail_page_url = detail_page_url.concat(strategy_keyname);
          var cell_text = "<a href=";
	  cell_text = cell_text.concat(detail_page_url);
          cell_text = cell_text.concat(" target=_blank>Details</a>");
	  console.log(cell_text);
          tbody_tr.append("td").attr("rowspan", metrics.length)
			.attr("class", cell_class).html(cell_text);
	}
    }  
}  




