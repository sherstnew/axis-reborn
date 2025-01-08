export interface InputData {
  center: number[];
  construction_area?: {
    no_living_square: number;
    apartments: number;
    block_of_flats: number;
  };
  people?: number;
}
