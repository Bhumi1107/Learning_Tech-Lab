const test = require("node:test");
const assert = require("node:assert/strict");
const {findRoute} = require("./routing");
const campus = require("./network");

test("Dijkstra picks the fastest walk", () => {
  const result = findRoute(campus, "gate", "lab");
  assert.deepEqual(result.route, ["gate", "quad", "cafe", "lab"]);
  assert.equal(result.minutes, 6);
});

test("BFS minimizes hops, retaining the real walking time", () => {
  const result = findRoute(campus, "gate", "lab", "hops");
  assert.deepEqual(result.route, ["gate", "hall", "lab"]);
  assert.equal(result.minutes, 16);
});

test("excluding stairs changes the fastest route", () => {
  const result = findRoute(campus, "gate", "lab", "time", true);
  assert.deepEqual(result.route, ["gate", "hall", "arts", "lab"]);
  assert.equal(result.minutes, 12);
});

test("same origin and destination", () => {
  assert.deepEqual(findRoute(campus, "lab", "lab"), {route: ["lab"], minutes: 0, visited: ["lab"]});
});

test("disconnected network and invalid endpoint", () => {
  const network = {...campus, paths: []};
  assert.equal(findRoute(network, "gate", "lab").minutes, null);
  assert.throws(() => findRoute(campus, "nowhere", "lab"), /Unknown place/);
});

test("compare all campus pairs to exhaustive simple-path enumeration", () => {
  function walk(here, end, seen, minutes, opts, best) {
    if (here === end) {
      best.time = Math.min(best.time, minutes);
      best.hops = Math.min(best.hops, seen.size - 1);
      return;
    }
    for (const [a, b, cost, stairs] of campus.paths) {
      if ((here !== a && here !== b) || (opts.stepFree && stairs)) continue;
      const next = here === a ? b : a;
      if (!seen.has(next)) walk(next, end, new Set([...seen, next]), minutes + cost, opts, best);
    }
  }
  for (const {id: start} of campus.places) {
    for (const {id: end} of campus.places) {
      for (const stepFree of [true, false]) {
        const best = {time: Infinity, hops: Infinity};
        walk(start, end, new Set([start]), 0, {stepFree}, best);
        assert.equal(findRoute(campus, start, end, "time", stepFree).minutes, best.time);
        assert.equal(findRoute(campus, start, end, "hops", stepFree).route.length - 1, best.hops);
      }
    }
  }
});
