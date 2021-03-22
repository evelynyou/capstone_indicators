/* Handle the search button click */

function render_custom_parameters() { 
    // base_url = "http://ec2-100-20-59-199.us-west-2.compute.amazonaws.com:8888/backtest?stock_ticker=";
    strategy =  document.getElementById("details_strategy").value;

    d3.select("#custom_parameters").html("");

    var parameters_map = {
	    "BuyAndHold": "",
	    "SmaCross": `<div style="text-align:right">
	                    Short SMA &nbsp;&nbsp; <input type='text' id='sma_short_sma' value='3' class='parameter_input'>  <br>
	                    Long SMA &nbsp;&nbsp; <input type='text' id='sma_long_sma' value='15' class='parameter_input'> <br>
                        Long Only &nbsp; &nbsp; <select id="sma_long_only" class='parameter_input'> 
                                <option value="Yes">Yes</option>
                                <option value="No">No</option>
                        </select>
	                 </div>`,
	    "MacdSignal": `<div style="text-align:right">
	                    Fast Period &nbsp;&nbsp; <input type='text' id='macd_fast_period' value='12' class='parameter_input'>  <br>
	                    Slow Period &nbsp;&nbsp; <input type='text' id='macd_slow_period' value='26'  class='parameter_input'> <br>
	                    Signal Period &nbsp;&nbsp; <input type='text' id='macd_signal_period' value='9'  class='parameter_input'> <br>
                        Long Only &nbsp; &nbsp; <select id="macd_long_only" class='parameter_input'> 
                                <option value="Yes">Yes</option>
                                <option value="No">No</option>
                        </select>
	                 </div>`,
	    "StochOsci": `<div style="text-align:right">
	                    Fast K Period &nbsp;&nbsp; <input type='text' id='osci_fast_k_period' value='14'  class='parameter_input'>  <br>
	                    Slow K Period &nbsp;&nbsp; <input type='text' id='osci_slow_k_period' value='3'  class='parameter_input'> <br>
	                    Slow D Period &nbsp;&nbsp; <input type='text' id='osci_slow_d_period' value='3'  class='parameter_input'> <br>
	                    Overbought &nbsp;&nbsp; <input type='text' id='osci_overbought' value='80'  class='parameter_input'> <br>
	                    Oversold &nbsp;&nbsp; <input type='text' id='osci_oversold' value='20'  class='parameter_input'> <br>
                        Long Only &nbsp; &nbsp; <select id="stoch_osci_long_only" class='parameter_input'> 
                                <option value="Yes">Yes</option>
                                <option value="No">No</option>
                        </select>
	                 </div>`,
	    "StochRsi": `<div style="text-align:right">
	                    Time Period &nbsp;&nbsp; <input type='text' id='rsi_time_period' value='14'  class='parameter_input'>  <br>
	                    Fast K Period &nbsp;&nbsp; <input type='text' id='rsi_fast_k_period' value='14'  class='parameter_input'> <br>
	                    Fast D Period &nbsp;&nbsp; <input type='text' id='rsi_fast_d_period' value='3'  class='parameter_input'> <br>
	                    Overbought &nbsp;&nbsp; <input type='text' id='rsi_overbought' value='80'  class='parameter_input'> <br>
	                    Oversold &nbsp;&nbsp; <input type='text' id='rsi_oversold' value='20'  class='parameter_input'> <br>
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
    window.alert("refresh");
}
 

