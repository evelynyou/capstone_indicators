/* Handle the search button click */

function render_custom_parameters() { 
    // base_url = "http://ec2-100-20-59-199.us-west-2.compute.amazonaws.com:8888/backtest?stock_ticker=";
    strategy =  document.getElementById("details_strategy").value;

    d3.select("#custom_parameters").html("");

    var parameters_map = {
	    "BuyAndHold": "",
	    "SmaCross": `<div style="text-align:right">
	                    Short SMA &nbsp;&nbsp; <input type='number' id='sma_short_sma' value='3' class='parameter_input'>  <br>
	                    Long SMA &nbsp;&nbsp; <input type='number' id='sma_long_sma' value='15' class='parameter_input'> <br>
                        Long Only &nbsp; &nbsp; <select id="sma_long_only" class='parameter_input'> 
                                <option value="Yes">Yes</option>
                                <option value="No">No</option>
                        </select>
	                 </div>`,
	    "MacdSignal": `<div style="text-align:right">
	                    Fast Period &nbsp;&nbsp; <input type='number' id='macd_fast_period' value='12' class='parameter_input'>  <br>
	                    Slow Period &nbsp;&nbsp; <input type='number' id='macd_slow_period' value='26'  class='parameter_input'> <br>
	                    Signal Period &nbsp;&nbsp; <input type='number' id='macd_signal_period' value='9'  class='parameter_input'> <br>
                        Long Only &nbsp; &nbsp; <select id="macd_long_only" class='parameter_input'> 
                                <option value="Yes">Yes</option>
                                <option value="No">No</option>
                        </select>
	                 </div>`,
	    "StochOsci": `<div style="text-align:right">
	                    Fast K Period &nbsp;&nbsp; <input type='number' id='osci_fast_k_period' value='14'  class='parameter_input'>  <br>
	                    Slow K Period &nbsp;&nbsp; <input type='number' id='osci_slow_k_period' value='3'  class='parameter_input'> <br>
	                    Slow D Period &nbsp;&nbsp; <input type='number' id='osci_slow_d_period' value='3'  class='parameter_input'> <br>
	                    Overbought &nbsp;&nbsp; <input type='number' id='osci_overbought' value='80'  class='parameter_input'> <br>
	                    Oversold &nbsp;&nbsp; <input type='number' id='osci_oversold' value='20'  class='parameter_input'> <br>
                        Long Only &nbsp; &nbsp; <select id="stoch_osci_long_only" class='parameter_input'> 
                                <option value="Yes">Yes</option>
                                <option value="No">No</option>
                        </select>
	                 </div>`,
	    "StochRsi": `<div style="text-align:right">
	                    Time Period &nbsp;&nbsp; <input type='number' id='rsi_time_period' value='14'  class='parameter_input'>  <br>
	                    Fast K Period &nbsp;&nbsp; <input type='number' id='rsi_fast_k_period' value='14'  class='parameter_input'> <br>
	                    Fast D Period &nbsp;&nbsp; <input type='number' id='rsi_fast_d_period' value='3'  class='parameter_input'> <br>
	                    Overbought &nbsp;&nbsp; <input type='number' id='rsi_overbought' value='80'  class='parameter_input'> <br>
	                    Oversold &nbsp;&nbsp; <input type='number' id='rsi_oversold' value='20'  class='parameter_input'> <br>
                        Long Only &nbsp; &nbsp; <select id="stoch_rsi_long_only" class='parameter_input'> 
                                <option value="Yes">Yes</option>
                                <option value="No">No</option>
                        </select>
	                 </div>`
    };

    parameters_html = parameters_map[strategy];
    d3.select("#custom_parameters").html(parameters_html);
}

function refresh() {
    strategy =  document.getElementById("details_strategy").value;
    stock_ticker =  document.getElementById("details_ticker").value;
    d3.select("#vs_buy_and_hold").html("");

    switch(strategy) {
        case "SmaCross":
            // code block
            sma_slow = document.getElementById("sma_long_sma").value;
            sma_fast = document.getElementById("sma_short_sma").value;
            long_only = document.getElementById("sma_long_only").value;
            // TODO: add this parameter
            date_range = "1y"
            // http://ec2-100-20-59-199.us-west-2.compute.amazonaws.com:8888/vs_buy_and_hold?stock_ticker=SPY&strategy=SmaCross&date_range=1y&sma_slow=15&sma_fast=3&long_only=Yes
            url = "/vs_buy_and_hold?"
                    .concat("stock_ticker=").concat(stock_ticker)
                    .concat("&strategy=").concat(strategy)
                    .concat("&sma_slow=").concat(sma_slow)
                    .concat("&sma_fast=").concat(sma_fast)
                    .concat("&long_only=").concat(long_only)
                    .concat("&date_range=").concat(date_range);

            console.log(url);

            d3.json(url, function(err, data) {
                if (err) throw err;
                console.log(data);
                d3.select("#vs_buy_and_hold").text(JSON.stringify(data));
            });
            break;
        case "MacdSignal":
            // code block
            break;
        case "StochOsci":
            // code block
            break;
        case "StochRsi":
            // code block
            break;
        default:
            window.alert("Not supported strategy: ".concat(strategy));
    }
}
 

