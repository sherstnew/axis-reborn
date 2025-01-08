const points = [
  [55.74656, 37.680364],
  [55.751411, 37.685987],
  [55.753643, 37.673654],
  [55.750167, 37.670645],
  [55.74656, 37.680364],
];

let sum_x = 0;
let sum_y = 0;
let points_len = points.length;

points.forEach(point => {
  sum_x += point[0];
  sum_y += point[1];
})

const center = [sum_x / points_len, sum_y / points_len];
