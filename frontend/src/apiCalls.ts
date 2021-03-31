import { bio_reactors, experiments } from "./components/Stores.js";

export async function getBioReactors() {
  const res = await fetch(process.env.API_URL + "/bio_reactors", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });
  if (res.ok) {
    bio_reactors.set(await res.json());
  } else {
    return undefined;
  }
}

export async function getExperiments() {
  const res = await fetch(process.env.API_URL + "/experiments", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });
  if (res.ok) {
    experiments.set(await res.json());
  } else {
    return undefined;
  }
}
