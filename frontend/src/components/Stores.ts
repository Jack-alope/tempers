import { writable, Writable } from "svelte/store";
import type {
  experiment_interface,
  bio_reactor_interface,
} from "../interfaces";

export const json_data_list = writable(0);
export const experiments: Writable<experiment_interface[]> =
  writable(undefined);
export const bio_reactors: Writable<bio_reactor_interface[]> =
  writable(undefined);
  
// REVIEW: Reacator to not use these stores
export const showExperiment: Writable<boolean> = writable(false);
export const showBioReactor: Writable<boolean> = writable(false);
