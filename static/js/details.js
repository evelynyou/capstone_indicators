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
                        Long Only &nbsp; &nbsp; <select id="long_only" class='parameter_input'> 
                                <option value="Yes">Yes</option>
                                <option value="No">No (Long + Short)</option>
                        </select> <br>

                        Date Range &nbsp; &nbsp; <select id="date_range" class='parameter_input'> 
                                <option value="6m">last 6 month</option>
                                <option value="1y">last 1 year</option>
                                <option value="2y">last 2 years </option>
                                <option value="2020">2020</option>
                                <option value="2019">2019</option>
                                <option value="2018">2018</option>
                                <option value="2017">2017</option>
                                <option value="2016">2016</option>
                        </select>

	                 </div>`,
	    "MacdSignal": `<div style="text-align:right">
	                    Fast Period &nbsp;&nbsp; <input type='number' id='macd_fast_period' value='12' class='parameter_input'>  <br>
	                    Slow Period &nbsp;&nbsp; <input type='number' id='macd_slow_period' value='26'  class='parameter_input'> <br>
	                    Signal Period &nbsp;&nbsp; <input type='number' id='macd_signal_period' value='9'  class='parameter_input'> <br>
                        Long Only &nbsp; &nbsp; <select id="long_only" class='parameter_input'> 
                                <option value="Yes">Yes</option>
                                <option value="No">No (Long + Short)</option>
                        </select><br>
                        Date Range &nbsp; &nbsp; <select id="date_range" class='parameter_input'> 
                                <option value="6m">last 6 month</option>
                                <option value="1y">last 1 year</option>
                                <option value="2y">last 2 years </option>
                                <option value="2020">2020</option>
                                <option value="2019">2019</option>
                                <option value="2018">2018</option>
                                <option value="2017">2017</option>
                                <option value="2016">2016</option>
                        </select>

	                 </div>`,
	    "StochOsci": `<div style="text-align:right">
	                    Fast K Period &nbsp;&nbsp; <input type='number' id='osci_fast_k_period' value='14'  class='parameter_input'>  <br>
	                    Slow K Period &nbsp;&nbsp; <input type='number' id='osci_slow_k_period' value='3'  class='parameter_input'> <br>
	                    Slow D Period &nbsp;&nbsp; <input type='number' id='osci_slow_d_period' value='3'  class='parameter_input'> <br>
	                    Overbought &nbsp;&nbsp; <input type='number' id='osci_overbought' value='80'  class='parameter_input'> <br>
	                    Oversold &nbsp;&nbsp; <input type='number' id='osci_oversold' value='20'  class='parameter_input'> <br>
                        Long Only &nbsp; &nbsp; <select id="long_only" class='parameter_input'> 
                                <option value="Yes">Yes</option>
                                <option value="No">No (Long + Short)</option>
                        </select><br>
                        Date Range &nbsp; &nbsp; <select id="date_range" class='parameter_input'> 
                                <option value="6m">last 6 month</option>
                                <option value="1y">last 1 year</option>
                                <option value="2y">last 2 years </option>
                                <option value="2020">2020</option>
                                <option value="2019">2019</option>
                                <option value="2018">2018</option>
                                <option value="2017">2017</option>
                                <option value="2016">2016</option>
                        </select>

	                 </div>`,
	    "StochRsi": `<div style="text-align:right">
	                    Time Period &nbsp;&nbsp; <input type='number' id='rsi_time_period' value='14'  class='parameter_input'>  <br>
	                    Fast K Period &nbsp;&nbsp; <input type='number' id='rsi_fast_k_period' value='14'  class='parameter_input'> <br>
	                    Fast D Period &nbsp;&nbsp; <input type='number' id='rsi_fast_d_period' value='3'  class='parameter_input'> <br>
	                    Overbought &nbsp;&nbsp; <input type='number' id='rsi_overbought' value='80'  class='parameter_input'> <br>
	                    Oversold &nbsp;&nbsp; <input type='number' id='rsi_oversold' value='20'  class='parameter_input'> <br>
                        Long Only &nbsp; &nbsp; <select id="long_only" class='parameter_input'> 
                                <option value="Yes">Yes</option>
                                <option value="No">No (Long + Short)</option>
                        </select><br>

                        Date Range &nbsp; &nbsp; <select id="date_range" class='parameter_input'> 
                                <option value="6m">last 6 month</option>
                                <option value="1y">last 1 year</option>
                                <option value="2y">last 2 years </option>
                                <option value="2020">2020</option>
                                <option value="2019">2019</option>
                                <option value="2018">2018</option>
                                <option value="2017">2017</option>
                                <option value="2016">2016</option>
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
            long_only = document.getElementById("long_only").value;
            date_range = document.getElementById("date_range").value;
            // /vs_buy_and_hold?stock_ticker=SPY&strategy=SmaCross&date_range=1y&sma_slow=15&sma_fast=3&long_only=Yes
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
            // common fields 
            long_only = document.getElementById("long_only").value;
            date_range = document.getElementById("date_range").value;
            // strategy specific
            fast_period = document.getElementById("macd_fast_period").value;
            slow_period = document.getElementById("macd_slow_period").value;
            signal_period = document.getElementById("macd_signal_period").value;

            // /vs_buy_and_hold?stock_ticker=SPY&strategy=MacdSignal&date_range=1y&long_only=Yes&fast_period=3&slow_period=15&signal_period=21
            url = "/vs_buy_and_hold?"
                    .concat("stock_ticker=").concat(stock_ticker)
                    .concat("&strategy=").concat(strategy)
                    .concat("&long_only=").concat(long_only)
                    .concat("&date_range=").concat(date_range)
                    .concat("&fast_period=").concat(fast_period)
                    .concat("&slow_period=").concat(slow_period)
                    .concat("&signal_period=").concat(signal_period);

            console.log(url);
            d3.json(url, function(err, data) {
                if (err) throw err;
                console.log(data);
                d3.select("#vs_buy_and_hold").text(JSON.stringify(data));
            });
            break;
        case "StochOsci":
            // common fields 
            long_only = document.getElementById("long_only").value;
            date_range = document.getElementById("date_range").value;
            // strategy specific
            fast_k_period = document.getElementById("osci_fast_k_period").value;
            slow_k_period = document.getElementById("osci_slow_k_period").value;
            slow_d_period = document.getElementById("osci_slow_d_period").value;
            overbought = document.getElementById("osci_overbought").value;
            oversold = document.getElementById("osci_oversold").value;

            // /vs_buy_and_hold?stock_ticker=SPY&strategy=StochOsci&date_range=1y&long_only=Yes&fast_k_period=3&slow_k_period=15&slow_d_period=21&overbought=80&oversold=20
            url = "/vs_buy_and_hold?"
                    .concat("stock_ticker=").concat(stock_ticker)
                    .concat("&strategy=").concat(strategy)
                    .concat("&long_only=").concat(long_only)
                    .concat("&date_range=").concat(date_range)
                    .concat("&fast_k_period=").concat(fast_k_period)
                    .concat("&slow_k_period=").concat(slow_k_period)
                    .concat("&slow_d_period=").concat(slow_d_period)
                    .concat("&overbought=").concat(overbought)
                    .concat("&oversold=").concat(oversold);

            console.log(url);
            d3.json(url, function(err, data) {
                if (err) throw err;
                console.log(data);
                d3.select("#vs_buy_and_hold").text(JSON.stringify(data));
            });
            break;
        case "StochRsi":
            // common fields 
            long_only = document.getElementById("long_only").value;
            date_range = document.getElementById("date_range").value;
            // strategy specific
            time_period = document.getElementById("rsi_time_period").value;
            fast_k_period = document.getElementById("rsi_fast_k_period").value;
            fast_d_period = document.getElementById("rsi_fast_d_period").value;
            overbought = document.getElementById("rsi_overbought").value;
            oversold = document.getElementById("rsi_oversold").value;

            // /vs_buy_and_hold?stock_ticker=SPY&strategy=StochRsi&date_range=1y&long_only=Yes&fast_k_period=3&slow_k_period=15&slow_d_period=21&overbought=80&oversold=20&time_period=10
            url = "/vs_buy_and_hold?"
                    .concat("stock_ticker=").concat(stock_ticker)
                    .concat("&strategy=").concat(strategy)
                    .concat("&long_only=").concat(long_only)
                    .concat("&date_range=").concat(date_range)
                    .concat("&time_period=").concat(time_period)
                    .concat("&fast_k_period=").concat(fast_k_period)
                    .concat("&fast_d_period=").concat(fast_d_period)
                    .concat("&overbought=").concat(overbought)
                    .concat("&oversold=").concat(oversold);

            console.log(url);
            d3.json(url, function(err, data) {
                if (err) throw err;
                console.log(data);
                d3.select("#vs_buy_and_hold").text(JSON.stringify(data));
            });
            break;
        default:
            window.alert("Not supported strategy: ".concat(strategy));
    }
}
 

