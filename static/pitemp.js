/*global Chart */
(function($) {

  //setInterval(function() {
  //  $.ajax('/temperature').done(function(data) {
  //    $('#current-temperature').html(data.celsius + '&#8451;');
  //  });
  //}, 1500);

  var ctx = document.getElementById('temperature-chart').getContext('2d');

  $.ajax('/data').done(function(data) {
    var labels = [];
    var chartData = {
      'celsius': [],
      'fahrenheit': []
    };
    var k;

    for (k in data) {
      if (data.hasOwnProperty(k)) {
        labels.push(k);
        chartData['celsius'].push(data[k]['celsius']);
        chartData['fahrenheit'].push(data[k]['fahrenheit']);
      }
    }

    var chart = new Chart(ctx).Line({
      labels: labels,
      datasets: [
        {
          label: 'Celsius',
          fillColor: 'rgba(220,220,220,0.2)',
          strokeColor: 'rgba(220,220,220,1)',
          pointColor: 'rgba(220,220,220,1)',
          pointStrokeColor: '#fff',
          pointHighlightFill: '#fff',
          pointHighlightStroke: 'rgba(220,220,220,1)',
          data: chartData['celsius']
        },
        {
          label: 'Fahrenheit',
          fillColor: 'rgba(151,187,205,0.2)',
          strokeColor: 'rgba(151,187,205,1)',
          pointColor: 'rgba(151,187,205,1)',
          pointStrokeColor: '#fff',
          pointHighlightFill: '#fff',
          pointHighlightStroke: 'rgba(151,187,205,1)',
          data: chartData['fahrenheit']
        }
      ]
    }, {
      multiTooltipTemplate: '<%= datasetLabel %> - <%= value %>'
    });
  });

}(jQuery));
