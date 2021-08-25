export interface experiment_interface {
  id: number;
  start_date: Date;
  has_vids: boolean;
}

export interface bio_reactor_interface {
  id: number;
  bio_reactor_number: number;
  date_added: Date;
  bio_reactor_note: string;
  post_distance: number;
  youngs_modulus: number;
  has_vids: boolean;
}

export interface video_interface {
  id: number;
  date_uploaded: Date;
  date_recorded: Date;
  frequency: number;
  // REVIEW: Might not need this
  calibration_distance: number;
  calibration_factor: number;
  experiment_idenifer: string;
  bio_reactor_number: number;
  tracked: boolean;
  anaylized: boolean;
  save_location: string;
  video_note: string;
}

export interface post_interface {
  id: number;
  post_number: number;
}

export interface vid_show {
  [experiment_idenifer: string]: video_interface[];
}
