export interface InputData {
  center: number[];
  points?: [number, number][];
  people?: number;
  construction_area?: {
    no_living_square: number;
    apartments: number;
    block_of_flats: number;
  };
}
