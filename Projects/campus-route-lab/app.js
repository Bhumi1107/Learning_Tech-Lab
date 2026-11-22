const byId = id => document.getElementById(id);
const places = new Map(campus.places.map(place => [place.id, place]));
const placeName = id => places.get(id).name;
const namespace = "http://www.w3.org/2000/svg";

function shape(type, attrs, label) {
  const element = document.createElementNS(namespace, type);
  for (const [key, value] of Object.entries(attrs)) element.setAttribute(key, value);
  if (label !== undefined) element.textContent = label;
  return element;
}

function draw(route) {
  const edges = byId("edges");
  const nodes = byId("nodes");
  edges.replaceChildren();
  nodes.replaceChildren();
  for (const [a, b, minutes, stairs] of campus.paths) {
    const start = places.get(a);
    const end = places.get(b);
    const index = route.indexOf(a);
    const active = index >= 0 && (route[index - 1] === b || route[index + 1] === b);
    edges.append(shape("line", {x1: start.x, y1: start.y, x2: end.x, y2: end.y,
      class: ["path", active && "active", stairs && "stair"].filter(Boolean).join(" ")}));
    edges.append(shape("text", {x: (start.x + end.x) / 2, y: (start.y + end.y) / 2 - 6,
      "text-anchor": "middle", class: "edge-label"}, minutes));
  }
  for (const {id, name, x, y} of places.values()) {
    nodes.append(shape("circle", {cx: x, cy: y, r: 8, class: route.includes(id) ? "place chosen" : "place"}));
    nodes.append(shape("text", {x, y: y + 23, class: "place-label", "text-anchor": "middle"}, name));
  }
}

function render() {
  const start = byId("from").value;
  const end = byId("to").value;
  const mode = byId("mode").value;
  const stepFree = byId("step-free").checked;
  const fastest = mode === "time";
  const result = findRoute(campus, start, end, mode, stepFree);
  const other = findRoute(campus, start, end, fastest ? "hops" : "time", stepFree);
  draw(result.route);
  byId("algorithm").textContent = fastest ? "Dijkstra · fastest walk" : "Breadth-first search · fewest paths";
  byId("duration").textContent = result.minutes === null ? "No route" : result.minutes + " min";
  const hops = result.route.length - 1;
  byId("count").textContent = hops < 0 ? "No walk meets these settings." :
    hops === 0 ? "Start and destination are the same." : hops + (hops === 1 ? " path" : " paths");
  const stops = result.route.map(id => {
    const li = document.createElement("li");
    li.textContent = placeName(id);
    return li;
  });
  byId("stops").replaceChildren(...stops);
  const altLabel = fastest ? "Fewest paths" : "Fastest walk";
  const altHops = other.route.length - 1;
  byId("comparison").textContent = other.minutes === null ? "" :
    altLabel + ": " + other.minutes + " min across " + altHops + (altHops === 1 ? " path." : " paths.");
  byId("explanation").textContent = fastest ?
    "Dijkstra expands the unvisited place with the lowest total walking time. It stops when it reaches the destination." :
    "Breadth-first search explores all places one path away before places two paths away. Each path counts as one step.";
  byId("visits").textContent = "Visited in order: " + result.visited.map(placeName).join(" → ");
}

for (const place of campus.places) {
  for (const field of ["from", "to"]) byId(field).add(new Option(place.name, place.id));
}
byId("from").value = "gate";
byId("to").value = "lab";
for (const field of ["from", "to", "mode", "step-free"]) byId(field).addEventListener("change", render);
render();
