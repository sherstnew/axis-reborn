interface OutputStation {
  [index: string]: string | number;
  name: string;
  delta_traffic: number;
  delta_percent: number;
  previous_traffic: number;
  new_traffic: number;
  latitude: number;
  longtitude: number;
}

interface OutputStop {
  [index: string]: string | number;
  name: string;
  traffic: number;
  latitude: number;
  longtitude: number;
}

export interface Result {
  stations: OutputStation[];
  stops: OutputStop[];
  people: number;
}
