export async function getBioReactors() {
  const res = await fetch(process.env.url + "/bio_reactors", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });
  if (res.ok) {
    return await res.json();
  } else {
    return false;
  }
}

export async function getExperiments() {
  const res = await fetch(process.env.url + "/experiments", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });
  if (res.ok) {
    return await res.json();
  } else {
    return false;
  }
}
