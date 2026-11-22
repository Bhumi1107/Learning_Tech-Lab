// A fictional, undirected walking network. Coordinates only position the drawing.
const campus = {
  places: [
    {id: "gate", name: "Main Gate", x: 83, y: 202},
    {id: "hall", name: "Lecture Hall", x: 217, y: 95},
    {id: "quad", name: "Quadrangle", x: 226, y: 264},
    {id: "arts", name: "Arts Studio", x: 369, y: 57},
    {id: "cafe", name: "Canteen", x: 383, y: 222},
    {id: "garden", name: "Gardens", x: 370, y: 365},
    {id: "lab", name: "Science Lab", x: 540, y: 113},
    {id: "library", name: "Library", x: 568, y: 330}
  ],
  // [endpoint, endpoint, minutes, uses stairs]
  paths: [
    ["gate", "hall", 4, false], ["gate", "quad", 2, false],
    ["hall", "arts", 4, false], ["hall", "lab", 12, false],
    ["quad", "cafe", 2, false], ["quad", "garden", 5, false],
    ["arts", "lab", 4, false], ["cafe", "lab", 2, true],
    ["cafe", "library", 3, true], ["garden", "library", 3, false],
    ["lab", "library", 5, false]
  ]
};
if (typeof module !== "undefined") module.exports = campus;
