import { writable } from 'svelte/store'

import type { Writable } from 'svelte/store'
import type { experiment_interface, bio_reactor_interface } from '../types/interfaces'

export const json_data_list = writable(0)
export const experiments: Writable<experiment_interface[]> = writable()
export const bio_reactors: Writable<bio_reactor_interface[]> = writable()
