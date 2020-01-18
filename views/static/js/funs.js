/*google.charts.load('current', {packages: ['corechart', 'bar']});
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

function drawChart(a) {
    var min = document.getElementById('opt'+a+'_min').value;
    var max = document.getElementById('opt'+a+'_max').value;
    var words = ['Опция'];
    var votes = ['Количество голосов'];
    var res = [];
    for (let i=min; i<=max;i++){
        words.push(document.getElementById(i+'_text').innerHTML);
    }
    words.push({ role: 'annotation' })
    for (let i=min; i<=max;i++){
        var str = document.getElementById(i.toString()+'_votes').innerHTML.toString()
        votes.push(Number(str.substr(str.length-1)));
    }

    for (let i=0; i<words.length;i++){
        res.push([words[i], votes[i]])
    }

    var data = google.visualization.arrayToDataTable(res);

    var cssClassNames = {
        'headerRow': 'bg-d',
        'tableRow': 'bg-d',
        'oddTableRow': 'bg-d',
        'selectedTableRow': 'bg-d',
        'hoverTableRow': 'bg-d',
        'headerCell': 'bg-d',
        'tableCell': 'bg-d',
        'rowNumberCell': 'bg-d'
    };


    var options = {
      title: 'Голосование',
      pieHole: 0.4,
      'showRowNumber': true,
      'allowHtml': true,
      'cssClassNames': cssClassNames,
      //backgroundColor: '#666',
      backgroundColor: 'transparent',
        legend         : 'none',
       chartArea      : {left: 10, top: 10, width: '95%', height: '95%'}

    };

    var chart = new google.visualization.PieChart(document.getElementById('chart_div'+a));
    chart.draw(data, options);
}

function loadAll(){
    var n = document.getElementById('len').value;
    for (var i=1; i<=n; i++){
        //drawAxisTickColors(i);
        drawChart(i);
    }
}*/

