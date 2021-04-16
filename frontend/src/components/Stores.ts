import { writable } from "svelte/store";
import type {
  experiment_interface,
  bio_reactor_interface,
} from "../interfaces";

export const video_id = writable(0);
export const json_data_list = writable(0);
export const experiments = writable(undefined);
export const bio_reactors = writable(undefined);
export const videos = writable(undefined);

export const showExperiment = writable(false);
export const showBioReactor = writable(false);
