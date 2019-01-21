// @param: string
function getTweetView(buttonId) {
  var rows = $(".tweet-price-setter");
  rows.each(function( i ) {
      $(this).hide();
    });
  rows.each(function( i ) {
    switch (buttonId) {
      case ("button-default-view"):
        if ($(this).attr("data-price") == "-1.0") {
          $(this).show();
        }
        break;

      case ("button-all-view"):
        $(this).show();
        break;

      case ("button-price-adjusted-view"):
        if ($(this).attr("data-price") != "-1.0") {
          $(this).show();
        }
        break;

      case ("button-real-prices-view"):
        if ($(this).attr("data-price") != "-1.0" && $(this).attr("data-price") != "-2.0") {
          $(this).show();
        }
        break;
    }

  });
}

$(document).ready(function() {

  getTweetView("button-default-view");

  $(".view-choice-button").on('click', function() {
    getTweetView($(this).attr('id'));
  }
  );

  $('#filter-options').hide();
  $('#dropdown').on('click', function(){
    $('#filter-options').show();
    $('.current').hide()
  });
  $('#filter-options li').on('click', function(option){
    $('#current-view').text($(this).text());
    $('#filter-options').hide();
    ('.current').removeClass('current')
    $(this).addClass('current');
    option.preventDefault();
  })
});
