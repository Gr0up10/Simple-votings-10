google.charts.load('current', {packages: ['corechart', 'bar']});
google.charts.setOnLoadCallback(drawAxisTickColors);

function drawAxisTickColors(a) {
    var min = document.getElementById('opt'+a+'_min').value;
    var max = document.getElementById('opt'+a+'_max').value;
    var words = [];
    var votes = ['Голоса:'];
    for (let i=min; i<=max;i++){
        words.push(document.getElementById(i+'_text').innerHTML);
    }
    words.push({ role: 'annotation' })
    for (let i=min; i<=max;i++){
        var str = document.getElementById(i.toString()+'_votes').innerHTML.toString()
        votes.push(Number(str.substr(str.length-1)));
    }

    var data = google.visualization.arrayToDataTable([words, votes]);

    var options = {
    isStacked: 'percent',
    height: 200,
    legend: { position: 'top', maxLines: 2 },
    hAxis: {
            minValue: 0,
            ticks: [0, .3, .6, .9, 1]
          }
    };
    var chart = new google.visualization.BarChart(document.getElementById('chart_div'+a));
    chart.draw(data, options);
}