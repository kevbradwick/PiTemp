(function($) {

  setInterval(function() {
    $.ajax('/temperature').done(function(data) {
      $('#current-temperature').html(data.celsius + '&#8451;');
    });
  }, 1500);

}(jQuery));
