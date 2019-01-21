function tweetChanged() {
    var tweet_div = $('.tweet')
    var tweet_id = tweet_div.attr('id')
    var url = '/data/' + tweet_id
    var embedLink = $.getJSON(url, function(data) {
      tweet_div.html(data.embed_link);
    })
}

var tweetDiv = $('.tweet')[0];
var config = { attributes: true, childList: false, subtree: false };
var observer = new MutationObserver(tweetChanged);
observer.observe(tweetDiv, config);
