// Set up the SVG
const width = 960;
const height = 600;
const svg = d3.select("#graph")
    .append("svg")
    .attr("width", width)
    .attr("height", height);

// Color scale for NodeGroups
const color = d3.scaleOrdinal(d3.schemeCategory10);

// Create a div for the tooltip
const tooltip = d3.select("body").append("div")
    .attr("class", "tooltip")
    .style("opacity", 0)
    .style("position", "absolute")
    .style("background-color", "white")
    .style("border", "solid")
    .style("border-width", "1px")
    .style("border-radius", "5px")
    .style("padding", "10px");

// Load data
Promise.all([
    d3.csv("nodes.csv"),
    d3.csv("links.csv")
]).then(([nodes, links]) => {
    // Process nodes
    nodes.forEach(node => {
        node.radius = node.NodeType === 'app' ? Math.sqrt(node.NodeCost) * 2 : 3;
    });



    // Create the simulation
    const simulation = d3.forceSimulation(nodes)
        .force("link", d3.forceLink(links).id(d => d.id))
        .force("charge", d3.forceManyBody().strength(-100))
        .force("center", d3.forceCenter(width / 2, height / 2));

    // Add links
    const link = svg.append("g")
        .selectAll("line")
        .data(links)
        .join("line")
        .attr("stroke", "#999")
        .attr("stroke-opacity", 0.6);

    // Add nodes
    const node = svg.append("g")
        .selectAll("circle")
        .data(nodes)
        .join("circle")
        .attr("r", d => d.radius)
        .attr("fill", d => d.NodeType === 'app' ? color(d.NodeGroup) : "#B0C4DE")
        .call(drag(simulation))
        .on("mouseover", showTooltip)
        .on("mouseout", hideTooltip)
        .on("click", toggleTooltip);

    // Update positions on tick
    simulation.on("tick", () => {
        link
            .attr("x1", d => d.source.x)
            .attr("y1", d => d.source.y)
            .attr("x2", d => d.target.x)
            .attr("y2", d => d.target.y);

        node
            .attr("cx", d => d.x)
            .attr("cy", d => d.y);
    });

    // Tooltip functions
    function showTooltip(event, d) {
        tooltip.transition()
            .duration(200)
            .style("opacity", .9);
        tooltip.html(`Name: ${d.id}<br/>Cost: ${d.NodeCost}<br/>Group: ${d.NodeGroup}`)
            .style("left", (event.pageX + 10) + "px")
            .style("top", (event.pageY - 28) + "px");
    }

    function hideTooltip() {
        tooltip.transition()
            .duration(500)
            .style("opacity", 0);
    }

    let tooltipVisible = false;

    function toggleTooltip(event, d) {
        tooltipVisible = !tooltipVisible;
        if (tooltipVisible) {
            showTooltip(event, d);
        } else {
            hideTooltip();
        }
    }
});

// Drag function for nodes
function drag(simulation) {
    function dragstarted(event) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        event.subject.fx = event.subject.x;
        event.subject.fy = event.subject.y;
    }

    function dragged(event) {
        event.subject.fx = event.x;
        event.subject.fy = event.y;
    }

    function dragended(event) {
        if (!event.active) simulation.alphaTarget(0);
        event.subject.fx = null;
        event.subject.fy = null;
    }

    return d3.drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended);
}

// Add legend
//Get unique NodeGroups
const NodeGroups = [...new Set(nodes.map(d => d.NodeGroup))];

const legend = svg.append("g")
    .attr("class", "legend")
    .attr("transform", `translate(20, 20)`);  // Changed from (width - 120, 20) to (20, 20)

const legendItems = legend.selectAll(".legend-item")
    .data(NodeGroups)
    .enter().append("g")
    .attr("class", "legend-item")
    .attr("transform", (d, i) => `translate(0, ${i * 20})`);

legendItems.append("rect")
    .attr("width", 10)
    .attr("height", 10)
    .attr("fill", d => color(d));

legendItems.append("text")
    .attr("x", 15)
    .attr("y", 9)
    .text(d => d)
    .style("font-size", "12px");