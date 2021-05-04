import { bio_reactors, experiments, videos } from "./components/Stores.js";

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

export async function getVideos() {
  const res = await fetch(process.env.API_URL + "/videos_show", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });
  if (res.ok) {
    videos.set(await res.json());
  } else {
    return undefined;
  }
}

export async function getPostOptions(bio_id: string) {
  const res = await fetch(process.env.API_URL + `/posts?bio_id=${bio_id}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });
  if (res.ok) {
    return await res.json();
  } else {
    return undefined;
  }
}

export async function checkExpExist(exp_idenifer: string) {
  const res = await fetch(
    process.env.API_URL +
      `/experiment_exist?experiment_identifier=${exp_idenifer}`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    }
  );
  if (res.ok) {
    return await res.json();
  } else {
    return undefined;
  }
}
