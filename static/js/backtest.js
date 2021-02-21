/* Handle the search button click */
function backtest() {
    console.log();
    base_url = "/backtest_sma?stock_ticker=";
    ticker = document.getElementById("ticker").value;
    data_url = base_url.concat(ticker);

    console.log(ticker);
    console.log(data_url);
    
    d3.json(data_url,
            function(err, data) {
                if (err) throw err;
                console.log(data);
                document.getElementById("indicator_table").innerHTML = JSON.stringify(data);
            }
    );
}
