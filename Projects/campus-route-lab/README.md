# Campus Route Lab

The Science Lab is two paths from the Main Gate, yet taking three paths gets you there ten minutes sooner. This interactive map lets you change the endpoints, avoid stairs, and see which places each search visits.

**Try it locally.** Download and extract Learning_Tech-Lab, then open `Projects/campus-route-lab/index.html` in a browser. The planner works offline. The eight places and eleven walking paths describe a fictional campus.

## A walk that explains the difference

Start at **Main Gate** and end at **Science Lab**.

| Setting | Route | Walking time |
| --- | --- | ---: |
| Fastest walk | Main Gate → Quadrangle → Canteen → Science Lab | 6 min |
| Fewest paths | Main Gate → Lecture Hall → Science Lab | 16 min |
| Fastest walk with “Avoid stairs” | Main Gate → Lecture Hall → Arts Studio → Science Lab | 12 min |

The two-path walk includes a single 12-minute segment. Dijkstra’s algorithm adds up walking minutes, so it can choose a faster route with more stops. Breadth-first search counts each path once, regardless of its length.

## Explore the map

1. Pick a start and destination. Switch between **Fastest walk** and **Fewest paths**.
2. Select **Avoid stairs** to remove all stair segments from both searches.
3. Expand **How did the search reach this result?** to see the order in which it visited places. The map labels each path with its walking time.

## Implementation

| File | What it contains |
| --- | --- |
| [network.js](network.js) | Place coordinates, walking times, and stair flags for the undirected graph |
| [routing.js](routing.js) | Adjacency list, search frontier, and route reconstruction |
| [app.js](app.js) | Form controls, SVG drawing, comparison, and search trace |
| [routing.test.js](routing.test.js) | Known routes, same-location and disconnected cases, and an exhaustive comparison |

BFS processes waiting places in insertion order, using a JavaScript Set as a FIFO queue. It runs in O(V + E). Dijkstra chooses the lowest-cost waiting place using a linear scan, which gives O(V² + E) time. Each search uses O(V + E) space. Equal-cost routes keep the first one discovered.

## Check the routes

With Node.js 18 or newer, run the tests from the project directory.

```bash
node --test routing.test.js
```

The final test enumerates all simple paths for every pair of places. It checks the shortest walking time and the smallest number of paths, with stairs both included and excluded.
