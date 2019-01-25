// Built thanks to the following sample blocks:
// http://bl.ocks.org/weiglemc/6185069
// https://bl.ocks.org/d3noob/402dd382a51a4f6eea487f9a35566de0
// http://plnkr.co/edit/TMp2rt1SjpSNE3AkjlgZ?p=preview


// set the dimensions and margins of the graph
// and create the svg inside the graph div
var svg = d3.select('#graph').append("svg")
.attr('width', 1000)
.attr('height', 500)
var margin = {top: 20, right: 20, bottom: 45, left: 35},
width = +svg.attr("width") - margin.left - margin.right,
height = +svg.attr("height") - margin.top - margin.bottom,
g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// set the ranges
var x = d3.scaleTime().range([0, width]);
var y = d3.scaleLinear().range([height, 0]);

// define the line
var priceLine = d3.line()
.x(function(d) { return x(d.date); })
.y(function(d) { return y(d.price); })
.defined(function(d) {
  return d.price || d.price === '0';
});

// Set time date/time formats
var dateFormat = d3.timeFormat("%b %d %Y"),
timeAndDateFormat = d3.timeFormat("%b %d %Y %I:%M %p CST");

// add the tooltip area to the webpage
var tooltip = d3.select("body").append("div")
.attr("class", "tooltip")
.style("opacity", 0);

// select the tweet div
var tweet = d3.select('.tweet')

// Get the data
d3.json("/data", function(error, data) {
  if (error) throw error;

  // format the data
  sorteddata = data.sort(function(x, y){
    return d3.ascending(x.date, y.date);
  })

  var cleandata = [];
  sorteddata.forEach(function(d) {
    if (d.price >= 0) {
      cd = {}
      cd.date = new Date(+d.timestamp*1000 + 946703400000);
      cd.price = d.price;
      cd.id = d.id;
      cleandata.push(cd)
    };
  });

  console.log(cleandata)

  // Scale the range of the data
  x.domain(d3.extent(cleandata, function(d) { return d.date; }));
  y.domain([0, d3.max(cleandata, function(d) { return d.price; }) + 1]);

  // Add the valueline path.
  svg.append("path")
  .data([cleandata])
  .attr("class", "line")
  .attr("transform", "translate(" + margin.left + ",0)")
  .attr("d", priceLine);

  // Add the X Axis
  svg.append("g")
  .attr("transform", "translate(" + margin.left + "," + height + ")")
  .call(d3.axisBottom(x)
    .tickFormat(dateFormat)
    .ticks(10))
  .selectAll("text")
    .style("text-anchor", "end")
    .attr("dx", "-.8em")
    .attr("dy", ".15em")
    .attr("transform", "rotate(-65)");

  // Add the Y Axis
  svg.append("g")
  .attr("transform", "translate(" + margin.left + ",0)")
  .call(d3.axisLeft(y)
    .tickFormat(d3.format("($.2f")));

  // Add the dots.
  svg.selectAll(".dot")
  .data(cleandata)
  .enter().append("circle")
  .filter(function(d) { return d.price >= 0 })
  .attr("transform", "translate(" + margin.left + ",0)")
  .attr("r", 5)
  .attr("cx", function(d) { return x(d.date); })
  .attr("cy", function(d) { return y(d.price); })
  .attr("class", "dot")
  .style("fill", "darkgreen")
  .on("mouseover", function(d) {
    d3.select(this).attr("r", 15).style("fill", "url(#avocado-img)");
    tooltip.transition()
    .duration(200)
    .style("opacity", 1);
    tooltip.html("Price: $" + d.price + "<br/> Date: " + timeAndDateFormat(d.date)
    + "<br/> Click for source")
    .style("background", "yellowgreen")
    .style("position", "absolute")
    .style("border-radius", "3px")
    .style("padding", "4px")
    .style("left", (d3.event.pageX + 10) + "px")
    .style("top", (d3.event.pageY + 10) + "px");
  })
  .on("mouseout", function(d) {
    d3.select(this).attr("r", 5).style("fill", "darkgreen");
    tooltip.transition()
    .duration(100)
    .style("opacity", 0);
  })
  .on("click", function(d) {
    tweet.attr("id", d.id);
  });

});
