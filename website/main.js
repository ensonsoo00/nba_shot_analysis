// Parse the Data
d3.csv("../data/shots-2019-preprocessed.csv").then(function(data) {
    // Filter data for 'Knicks' team and three-pointers only
    var threePointData = data.filter(function(d) { return d.team === 'New York' && d.attempt === '3-pointer'; });
  
    // Filter data for 'Knicks' team and two-pointers only
    var twoPointData = data.filter(function(d) { return d.team === 'New York' && d.attempt === '2-pointer'; });
  
    // Count the number of 3-pointers for each player
    var threePointShotData = Array.from(d3.rollup(threePointData, 
      v => ({
        player: v[0].shots_by,
        shots: v.length
      }), 
      d => d.shots_by
    ), ([key, value]) => (value));
  
    // Count the number of 2-pointers for each player
    var twoPointShotData = Array.from(d3.rollup(twoPointData, 
      v => ({
        player: v[0].shots_by,
        shots: v.length
      }), 
      d => d.shots_by
    ), ([key, value]) => (value));
  
    // Create a map of players to their shot counts for two-pointers
    var twoPointShotMap = new Map(twoPointShotData.map(item => [item.player, item.shots]));
    var threePointShotMap = new Map(threePointShotData.map(item => [item.player, item.shots]));
    // Merge the two datasets
    // var mergedData = threePointShotData.map(item => ({
    //     player: item.player,
    //     threePointShots: item.shots,
    //     twoPointShots: twoPointShotMap.get(item.player) || 0
    // }));
    // Merge the two datasets
    var mergedData = twoPointShotData.map(item => ({
      player: item.player,
      twoPointShots: item.shots,
      threePointShots: threePointShotMap.get(item.player) || 0
    }));
  
    // Sort the mergedData array by twoPointShots in descending order
    mergedData.sort((a, b) => b.twoPointShots - a.twoPointShots);
  
    // Define the dimensions of the SVG
    var margin = {top: 50, right: 50, bottom: 50, left: 40},
        width = 1000 - margin.left - margin.right,
        height = 600 - margin.top - margin.bottom;
  
    // Create scales
    const xScale = d3.scaleBand()
      .domain(mergedData.map(d => d.player))
      .range([margin.left, width - margin.right])
      .padding(0.1);
  
    const yScale = d3.scaleLinear()
      .domain([0, d3.max(mergedData, d => Math.max(d.threePointShots, d.twoPointShots))])
      .range([height - margin.bottom, margin.top]);
  
    // Create SVG
    var svg = d3.select('#plot')
      .attr('width', width + margin.left + margin.right)
      .attr('height', height + margin.top + margin.bottom)
      .append('g')
      .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');
  
    // Create bars for three-pointers
    svg.selectAll('.threePointBox')
      .data(mergedData)
      .enter().append('rect')
        .attr('class', 'threePointBox')
        .attr('x', d => xScale(d.player))
        .attr('y', d => yScale(d.threePointShots))
        .attr('width', xScale.bandwidth() / 2)
        .attr('height', d => height - margin.bottom - yScale(d.threePointShots))
        .attr('fill', '#4daf4a');
  
    // Create bars for two-pointers
    svg.selectAll('.twoPointBox')
      .data(mergedData)
      .enter().append('rect')
        .attr('class', 'twoPointBox')
        .attr('x', d => xScale(d.player) + xScale.bandwidth() / 2)
        .attr('y', d => yScale(d.twoPointShots))
        .attr('width', xScale.bandwidth() / 2)
        .attr('height', d => height - margin.bottom - yScale(d.twoPointShots))
        .attr('fill', '#377eb8');
  
    // Add text labels for three-pointers
    svg.selectAll('.threePointLabel')
      .data(mergedData)
      .enter().append('text')
        .attr('class', 'threePointLabel')
        .attr('x', d => xScale(d.player) + xScale.bandwidth() / 4)
        .attr('y', d => yScale(d.threePointShots) - 5)
        .style('text-anchor', 'middle')
        .text(d => d.threePointShots)
        .style("font-size", "12px");
  
    // Add text labels for two-pointers
    svg.selectAll('.twoPointLabel')
      .data(mergedData)
      .enter().append('text')
        .attr('class', 'twoPointLabel')
        .attr('x', d => xScale(d.player) + 3 * xScale.bandwidth() / 4)
        .attr('y', d => yScale(d.twoPointShots) - 5)
        .style('text-anchor', 'middle')
        .text(d => d.twoPointShots)
        .style("font-size", "12px");
  
    // Create X axis
    svg.append("g")
      .attr("transform", "translate(0," + (height - margin.bottom) + ")")
      .call(d3.axisBottom(xScale))
      .selectAll('text')
        .style('text-anchor', 'end')
        .attr('transform', 'rotate(-45)');
  
    // Create Y axis
    svg.append("g")
      .attr("transform", "translate(" + margin.left + ",0)")
      .call(d3.axisLeft(yScale));

    // Add X axis label
    svg.append("text")             
    .attr("transform",
        "translate(" + (width/2) + " ," + 
                        (height + margin.top - 20) + ")")
    .style("text-anchor", "middle")
    .style('font-size', '13px')
    .text("Players");

    // Add Y axis label
    svg.append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", 0 - margin.left + 10)
    .attr("x",0 - (height / 2)+30)
    .attr("dy", "1em")
    .style('font-size', '13px')
    .style("text-anchor", "middle")
    .text("Shots Taken");
  
    // Add title
    svg.append('text')
      .attr('x', width / 2)
      .attr('y', margin.top / 2)
      .attr('text-anchor', 'middle')
      .style('font-size', '20px')
      .style('text-decoration', 'underline')
      .text('Shots Distribution for New York Knicks 2019-2020');

// Add legends
var legend = svg.selectAll('.legend')
    .data(['3-Pointers', '2-Pointers'])
    .enter().append('g')
    .attr('class', 'legend')
    .attr('transform', function(d, i) { return 'translate(' + (margin.left-100) + ',' + (i * 20 + margin.top) + ')'; });

legend.append('rect')
    .attr('x', width - 18)
    .attr('width', 18)
    .attr('height', 18)
    .style('fill', function(d, i) { return i === 0 ? '#4daf4a' : '#377eb8'; });

legend.append('text')
    .attr('x', width - 24)
    .attr('y', 9)
    .attr('dy', '.35em')
    .style('text-anchor', 'end')
    .text(function(d) { return d; });
  
  }).catch(function(error){
    console.log(error);
  });

