/* Handle the search button click */
function backtest() {
    console.log(document.getElementById("ticker").value);
    d3.json(" http://44.242.149.4:8080/backtest_sma?stock_ticker=spy&last_days='1y'",
            function(err, data) {
                if (err) throw err;
                console.log(data);

                document.getElementById("indicator_table").innerHTML = JSON.stringify(data);

            }
    );
}
