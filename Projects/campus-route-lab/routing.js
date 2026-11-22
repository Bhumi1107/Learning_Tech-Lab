// Positive edge weights are walking minutes. The queue in BFS is FIFO.
function findRoute(network, start, end, mode = "time", stepFree = false) {
  const graph = new Map(network.places.map(({id}) => [id, []]));
  if (!graph.has(start) || !graph.has(end)) throw new Error("Unknown place");
  if (mode !== "time" && mode !== "hops") throw new Error("Unknown routing mode");
  for (const [from, to, minutes, stairs] of network.paths) {
    if (stepFree && stairs) continue;
    graph.get(from).push({to, minutes});
    graph.get(to).push({to: from, minutes});
  }

  const cost = new Map([[start, 0]]);
  const previous = new Map();
  const visited = [];
  const pending = new Set([start]);
  while (pending.size) {
    let current = pending.values().next().value;
    // On this small graph a linear minimum scan keeps Dijkstra easy to inspect.
    if (mode === "time") {
      for (const candidate of pending) {
        if (cost.get(candidate) < cost.get(current)) current = candidate;
      }
    }
    pending.delete(current);
    visited.push(current);
    if (current === end) break;
    for (const edge of graph.get(current)) {
      const nextCost = cost.get(current) + (mode === "time" ? edge.minutes : 1);
      if (nextCost >= (cost.get(edge.to) ?? Infinity)) continue;
      cost.set(edge.to, nextCost);
      previous.set(edge.to, {id: current, minutes: edge.minutes});
      pending.add(edge.to);
    }
  }
  if (!cost.has(end)) return {route: [], minutes: null, visited};
  const route = [end];
  let minutes = 0;
  while (route[route.length - 1] !== start) {
    const step = previous.get(route[route.length - 1]);
    route.push(step.id);
    minutes += step.minutes;
  }
  return {route: route.reverse(), minutes, visited};
}
if (typeof module !== "undefined") module.exports = {findRoute};
