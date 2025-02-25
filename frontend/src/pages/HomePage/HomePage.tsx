import styles from "./HomePage.module.scss";
import { Layout } from "../../components/Layout/Layout";
import { useEffect, useState } from "react";
import {
  TextInput,
  Button,
  Icon,
  Select,
  Label,
  Switch,
} from "@gravity-ui/uikit";
import { Plus, MathOperations } from "@gravity-ui/icons";
import { Polygon } from "../../static/types/Polygon";
import { renderToString } from "react-dom/server";
import { Result } from "../../static/types/Result";
import { PieChart, BarChart } from "@mui/x-charts";
import { InputData } from "../../static/types/InputData";

declare const ymaps: any;

const defaultPoints: [number, number][] = [
  [55.74656, 37.680364],
  [55.751411, 37.685987],
  [55.753643, 37.673654],
  [55.750167, 37.670645],
];

export const HomePage = () => {
  const [results, setResults] = useState<Result>();

  const [map, setMap] = useState<any>(null);

  const [polygons, setPolygons] = useState<Polygon[]>([
    {
      name: "Полигон 1",
      points: defaultPoints,
    },
  ]);

  const [currentPolygon, setCurrentPolygon] = useState(0);

  const [apartments, setApartments] = useState(0);
  const [blocks, setBlocks] = useState(0);
  const [noLiving, setNoLiving] = useState(0);

  const [squareMode, setSquareMode] = useState<boolean>(false);

  const [people, setPeople] = useState<number>(0);

  const [loading, setLoading] = useState<boolean>(false);

  function init() {
    const myMap = new ymaps.Map(
      "map",
      {
        center: [55.74966820000001, 37.678202799999994],
        zoom: 15,
        controls: [],
      },
      {
        searchControlProvider: "yandex#search",
      }
    );

  //   myMap.events.add(["dblclick"], function (event: any) {
  //     const placemark = new ymaps.Placemark(event.get("coords"), {
  //       balloonContentBody: renderToString(
  //         <div className={styles.balloon}>
  //           <select defaultValue="station" id="select">
  //             <option value="station">Станция</option>
  //           </select>
  //           <header className={styles.balloon_header}>Создать объект</header>
  //           <input
  //             type="text"
  //             placeholder="Название"
  //             className={styles.input}
  //             defaultValue={""}
  //             onChange={(evt) => setNewName(evt.target.value)}
  //             id="name"
  //           />
  //         </div>
  //       ),
  //       hintContent: "Создать улицу",
  //     });

  //     myMap.geoObjects.add(placemark);
  //     placemark.balloon.open();
  //     placemark.events.add(["balloonclose"], function () {
  //       myMap.geoObjects.remove(placemark);
  //     });
  //   });
    setMap(myMap);
  }

  // init map
  useEffect(() => {
    if (!map) {
      ymaps.ready(init);
    }
  }, []);

  // init polygon
  useEffect(() => {
    if (map && polygons.length === 1) {
      createPolygons(map, polygons);
    }
  }, [map]);

  function editPoint(
    value: string,
    polygon_index: number,
    point_index: number,
    index_xy: number
  ) {
    if (!isNaN(Number(value))) {
      setPolygons((polygons) => {
        if (map) {
          map.geoObjects.remove(map.geoObjects.get(0));
          createPolygons(map, polygons);
        }
        return polygons.map((polygon, index) => {
          if (index === polygon_index) {
            polygon.points = polygon.points.map((point, i) => {
              if (i === point_index) {
                point[index_xy] = Number(value);
                return point;
              } else {
                return point;
              }
            });
            return polygon;
          } else {
            return polygon;
          }
        });
      });
    }
  }

  function calcCenter(points: [number, number][]) {
    let sum_x = 0;
    let sum_y = 0;
    let points_len = points.length;

    points.forEach((point: [number, number]) => {
      sum_x += point[0];
      sum_y += point[1];
    });

    return [sum_x / points_len, sum_y / points_len];
  }

  function createPolygons(map: any, polygons: Polygon[]) {
    if (map) {
      map.geoObjects.removeAll();
      polygons.forEach((polygonData, polygonIndex) => {
        const polygon = new ymaps.Polygon(
          [polygonData.points],
          {
            hintContent: `Полигон ${polygonIndex + 1}`,
          },
          {
            fillColor:
              polygonIndex === currentPolygon ? "#00A36C70" : "#ef575470",
            strokeColor:
              polygonIndex === currentPolygon ? "#00A36C" : "#ef5754",
            strokeWidth: 5,
          }
        );

        polygon.events.add(["geometrychange"], function (event: any) {
          const coords =
            event.get("target").geometry._coordPath._coordinates[0];
          setPolygons((polygons) =>
            polygons.map((polygon, index) => {
              if (index === polygonIndex) {
                return {
                  name: polygonData.name,
                  points: coords.filter(
                    (_coord: any, index: number) => index !== coords.length - 1
                  ),
                };
              } else {
                return polygon;
              }
            })
          );
        });

        map.geoObjects.add(polygon);

        if (polygonIndex === currentPolygon) {
          polygon.editor.startEditing();
        }
      });
    }
  }

  function createPolygon() {
    if (map) {
      const mapCenter: [number, number] = map.getCenter();

      const side = 0.003476;

      const newPolygon: Polygon = {
        name: `Полигон ${polygons.length + 1}`,
        points: [
          [mapCenter[0] + side, mapCenter[1] - side],
          [mapCenter[0] + side, mapCenter[1] + side],
          [mapCenter[0] - side, mapCenter[1] + side],
          [mapCenter[0] - side, mapCenter[1] - side],
        ],
      };
      createPolygons(map, [...polygons, newPolygon]);
      setCurrentPolygon(polygons.length);
      setPolygons((polygons) => [...polygons, newPolygon]);
    }
  }

  useEffect(() => {
    if (map) {
      createPolygons(map, polygons);
    }
  }, [currentPolygon]);

  function calculateData() {
    if (
      !isNaN(apartments) &&
      !isNaN(blocks) &&
      !isNaN(noLiving) &&
      polygons.length > 0 &&
      (people > 0 || (apartments > 0 && blocks > 0 && noLiving > 0))
    ) {
      const data: InputData = {
        center: polygons[currentPolygon]
          ? calcCenter(polygons[currentPolygon].points)
          : [55.750167, 37.670645],
      };

      if (squareMode) {
        data.construction_area = {
          no_living_square: noLiving,
          apartments: apartments,
          block_of_flats: blocks,
        };
        data.points = polygons[currentPolygon].points;
      } else {
        data.people = people;
        data.points = polygons[currentPolygon].points;
      }

      setLoading(true);
      setResults(undefined);

      fetch(
        `${import.meta.env.VITE_PUBLIC_BACKEND_URL}/calc/${
          squareMode ? "square" : "people"
        }`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(data),
        }
      )
        .then((data) => data.json())
        .then((res: Result) => {
          setResults(res);
          if (map) {
            res.stations.forEach((station) => {
              let color = "black";
              if (station.delta_percent >= 50) {
                color = "red";
              } else if (
                station.delta_percent < 50 &&
                station.delta_percent >= 25
              ) {
                color = "orange";
              } else if (
                station.delta_percent < 25 &&
                station.delta_percent >= 15
              ) {
                color = "yellow";
              } else if (
                station.delta_percent < 15 &&
                station.delta_percent >= 0
              ) {
                color = "green";
              }
              const placemark = new ymaps.Placemark(
                [station.latitude, station.longtitude],
                {
                  balloonContentBody: renderToString(
                    <div
                      className={styles.balloon}
                      style={{ display: "flex", flexWrap: "wrap" }}
                    >
                      <div style={{ width: "100%" }}>
                        Станция {station.name}
                      </div>
                      <div style={{ width: "100%" }}>
                        Было {station.previous_traffic} чел.
                      </div>
                      <div style={{ width: "100%" }}>
                        На {station.delta_percent}%
                      </div>
                      <div style={{ width: "100%" }}>
                        На {station.delta_traffic} чел.
                      </div>
                      <div style={{ width: "100%" }}>
                        Стало {station.new_traffic} чел.
                      </div>
                    </div>
                  ),
                  hintContent: station.name,
                },
                {
                  preset: "islands#circleDotIcon",
                  iconColor: color,
                }
              );
              map.geoObjects.add(placemark);
            });

            res.stops.forEach((stop) => {
              let color = "black";
              if (stop.traffic >= 500) {
                color = "red";
              } else if (stop.traffic < 500 && stop.traffic >= 350) {
                color = "orange";
              } else if (stop.traffic < 350 && stop.traffic >= 200) {
                color = "yellow";
              } else if (stop.traffic < 200 && stop.traffic >= 0) {
                color = "green";
              }
              const placemark = new ymaps.Placemark(
                [stop.latitude, stop.longtitude],
                {
                  balloonContentBody: renderToString(
                    <div
                      className={styles.balloon}
                      style={{ display: "flex", flexWrap: "wrap" }}
                    >
                      <div style={{ width: "100%" }}>Остановка {stop.name}</div>
                      <div style={{ width: "100%" }}>
                        Увеличение на {stop.traffic} чел.
                      </div>
                    </div>
                  ),
                  hintContent: stop.name,
                },
                {
                  preset: "islands#circleIcon",
                  iconColor: color,
                }
              );
              map.geoObjects.add(placemark);
            });
          }
          setLoading(false);
        })
        .catch((err) => {
          console.log(err);
        });
    } else {
      alert("Проверьте вводимые данные!");
    }
  }

  return (
    <Layout>
      <div className={styles.location}>
        <div className={styles.map_wrapper}>
          <div className={styles.map} id="map"></div>
        </div>
        <div className={styles.points}>
          <header className={styles.points_header}>
            {polygons[currentPolygon]?.name}
          </header>
          <div className={styles.btns}>
            <Button size="l" onClick={createPolygon}>
              <Icon data={Plus} />
              Добавить полигон
            </Button>
            <Select
              value={[String(currentPolygon)]}
              size="l"
              options={polygons.map((polygon, index) => {
                return {
                  value: String(index),
                  content: polygon.name,
                };
              })}
              onUpdate={(value) => setCurrentPolygon(Number(value))}
            />
          </div>
          {polygons[currentPolygon]
            ? polygons[currentPolygon].points.map((point, index) => (
                <div className={styles.point} key={index}>
                  <label>Точка {index + 1}</label>
                  <TextInput
                    value={String(point[0])}
                    onChange={(evt) =>
                      editPoint(evt.target.value, currentPolygon, index, 0)
                    }
                    label="X: "
                  />
                  <TextInput
                    value={String(point[1])}
                    onChange={(evt) =>
                      editPoint(evt.target.value, currentPolygon, index, 1)
                    }
                    label="Y: "
                  />
                </div>
              ))
            : ""}
        </div>
      </div>
      <div className={styles.inputs}>
        <div className={styles.inputs_header}>Данные на ввод</div>
        <Switch
          content="По площади"
          onUpdate={(checked) => setSquareMode(checked)}
        />
        {squareMode ? (
          <>
            <label className={styles.inputs_subheader}>Жилплощадь</label>
            <div className={styles.block}>
              <TextInput
                onUpdate={(value) => setApartments(Number(value))}
                defaultValue="0"
                label="Апартаменты"
                type="number"
                endContent={<Label size="m">м²</Label>}
                size="l"
              />
            </div>
            <div className={styles.block}>
              <TextInput
                onUpdate={(value) => setBlocks(Number(value))}
                defaultValue="0"
                label="Многоквартирные"
                type="number"
                endContent={<Label size="m">м²</Label>}
                size="l"
              />
            </div>
            <div className={styles.block}>
              <TextInput
                onUpdate={(value) => setNoLiving(Number(value))}
                defaultValue="0"
                label="Нежилая площадь"
                type="number"
                endContent={<Label size="m">м²</Label>}
                size="l"
              />
            </div>
          </>
        ) : (
          <div className={styles.block}>
            <TextInput
              onUpdate={(value) => setPeople(Number(value))}
              defaultValue="0"
              label="Население"
              type="number"
              endContent={<Label size="m">чел.</Label>}
              size="l"
            />
          </div>
        )}
        <Button size="xl" onClick={calculateData}>
          <Icon data={MathOperations} size={20} />
          {loading ? "Рассчитываем..." : "Рассчитать данные"}
        </Button>
      </div>
      {results ? (
        <>
          <div className={styles.results}>
            <div className={styles.block}>
              <div className={styles.inputs_header}>Станции</div>
              <div className={styles.block}>
                {results.stations.map((station, index) => (
                  <div className={styles.block} key={index}>
                    <div className={styles.inputs_header}>{station.name}</div>
                    <div className={styles.block} style={{ paddingLeft: 30 }}>
                      <div className={styles.inputs_subheader}>
                        Пассажиропоток ~{station.new_traffic} чел.
                      </div>
                      <label style={{ paddingLeft: 30 }}>
                        Увеличение на {station.delta_traffic} человек
                      </label>
                      <label style={{ paddingLeft: 30 }}>
                        Увеличение на {station.delta_percent}%
                      </label>
                    </div>
                  </div>
                ))}
              </div>
            </div>
            <div className={styles.block}>
              <div className={styles.inputs_header}>Остановки</div>
              {results.stops.map((stop, index) => (
                <div
                  className={styles.block}
                  style={{ paddingLeft: 30 }}
                  key={index}
                >
                  <div className={styles.inputs_subheader}>
                    Остановка {stop.name}
                  </div>
                  <label style={{ paddingLeft: 30 }}>
                    Увеличение на {stop.traffic} человек
                  </label>
                </div>
              ))}
            </div>
          </div>
          <div className={styles.charts}>
            <h2 className={styles.charts_header}>
              Увеличение пассажиропотока на станциях, чел.
            </h2>
            {/* <PieChart
              series={[
                {
                  data: results.stations.map((station, index) => ({
                    id: index,
                    value: station.delta_traffic,
                    label: station.name,
                  })),
                },
              ]}
              height={300}
            /> */}
            <BarChart
              dataset={results.stations}
              xAxis={[{ scaleType: "band", dataKey: "name" }]}
              series={[
                { dataKey: "delta_traffic", label: "Новый траффик, чел." },
              ]}
              height={500}
            />
            <h2 className={styles.charts_header}>
              Увеличение пассажиропотока на остановках, чел.
            </h2>
            {/* <PieChart
              series={[
                {
                  data: results.stops.map((stop, index) => ({
                    id: index,
                    value: stop.traffic,
                    label: stop.name,
                  })),
                },
              ]}
              height={300}
            /> */}
            <BarChart
              dataset={results.stops}
              xAxis={[{ scaleType: "band", dataKey: "name" }]}
              series={[{ dataKey: "traffic", label: "Новый траффик, чел." }]}
              height={500}
            />
            <h2 className={styles.charts_header}>
              Увеличенный пассажиропоток на станциях, чел.
            </h2>
            <h2 className={styles.charts_header}>До:</h2>
            <PieChart
              colors={[
                "#ff0000",
                "#ff8700",
                "#ffd300",
                "#deff0a",
                "#a1ff0a",
                "#0aff99",
                "#0aefff",
                "#147df5",
                "#580aff",
                "#be0aff",
              ]}
              series={[
                {
                  data: results.stations.map((station, index) => ({
                    id: index,
                    value: station.previous_traffic,
                    label: station.name,
                  })),
                },
              ]}
              height={300}
            />
            <h2 className={styles.charts_header}>После:</h2>
            <PieChart
              colors={[
                "#ff0000",
                "#ff8700",
                "#ffd300",
                "#deff0a",
                "#a1ff0a",
                "#0aff99",
                "#0aefff",
                "#147df5",
                "#580aff",
                "#be0aff",
              ]}
              series={[
                {
                  data: results.stations.map((station, index) => ({
                    id: index,
                    value: station.new_traffic,
                    label: station.name,
                  })),
                },
              ]}
              height={300}
            />
            <h2 className={styles.charts_header}>
              Сравнение пассажиропотока до и после:
            </h2>
            <BarChart
              dataset={results.stations}
              xAxis={[{ scaleType: "band", dataKey: "name" }]}
              series={[
                {
                  dataKey: "previous_traffic",
                  label: "Текущий пассажиропоток, чел.",
                },
                {
                  dataKey: "new_traffic",
                  label: "Увеличенный пассажиропоток, чел.",
                },
              ]}
              height={500}
            />
          </div>
        </>
      ) : (
        ""
      )}
    </Layout>
  );
};
