export interface experiment_interface {
  id: number;
  experiment_idenifer: string;
  start_date: Date;
}

export interface bio_reactor_interface {
  id: number;
  bio_reactor_number: number;
  date_added: Date;
}

export interface video_interface {
  id: number;
  date_uploaded: Date;
  date_recorded: Date;
  frequency: number;
  calibration_distance: number;
  calibration_factor: number;
  experiment_idenifer: string;
  bio_reactor_number: number;
}
