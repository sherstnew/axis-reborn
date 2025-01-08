ymaps.ready(init);

function init() {
  var myMap = new ymaps.Map(
    "map",
    {
      center: [55.749616, 37.676776],
      zoom: 15,
      controls: [],
    },
    {
      searchControlProvider: "yandex#search",
    }
  );

  const myPolygon = new ymaps.Polygon(
    [
      [
        [55.74656, 37.680364],
        [55.751411, 37.685987],
        [55.753643, 37.673654],
        [55.750167, 37.670645],
      ],
    ],
    {
      hintContent: "Многоугольник",
    },
    {
      fillColor: "#d9d9d9",
      strokeColor: "#2f528f",
      strokeWidth: 5,
      opacity: 0.5,
    }
  );

  myPolygon.events.add(["geometrychange"], function (event) {
    console.log(event.get("target").geometry._coordPath._coordinates);
  });

  myMap.geoObjects.add(myPolygon);

  myPolygon.editor.startEditing();
}
