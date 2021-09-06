<script lang="ts">
  import { onMount } from "svelte";
  import Grapher from "../components/Grapher.svelte";

  import { experiments, json_data_list } from "../components/Stores.js";

  let video_id: number;

  let nums, freqs, types, experiment_id, tissue_number, date_recorded;

  async function handleVideoSelected(url: string) {
    const res = await fetch(process.env.API_URL + url, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (res.ok) {
      const response_json = await res.json();
      json_data_list.set(response_json.json_data_list);
      nums = response_json.nums;
      freqs = response_json.freqs;
      types = response_json.types;
    } else {
      alert("Something went wrong");
    }
  }

  onMount(async () => {
    const urlParams = new URLSearchParams(window.location.search);
    video_id = parseInt(urlParams.get("video_id"));
    experiment_id = urlParams.get("experiment_id");
    tissue_number = parseInt(urlParams.get("tissue_number"));
    date_recorded = urlParams.get("date_recorded");
    if (video_id) {
      await handleVideoSelected(`/analyze?video_id=${video_id}`);
    } else if (experiment_id && tissue_number && date_recorded) {
      await handleVideoSelected(
        `/analyze/tissue_number?tissue_number=${tissue_number}&experiment_id=${experiment_id}&date_recorded${date_recorded}`
      );
    } else {
      await handleVideoSelected(
        `/analyze/tissue_number?tissue_number=${tissue_number}&experiment_id=${experiment_id}`
      );
    }
  });
</script>

<svelte:head>
  <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
  <script
    src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"
    type="text/javascript">
  </script>
</svelte:head>

<h1>Analyze</h1>

{#if nums && freqs && types && video_id}
  <Grapher {nums} {freqs} {types} {video_id} />
{:else if date_recorded && nums && freqs && types && experiment_id && tissue_number}
  <Grapher
    {nums}
    {freqs}
    {types}
    {experiment_id}
    {tissue_number}
    {date_recorded}
  />
{:else if nums && freqs && types && experiment_id && tissue_number}
  <Grapher {nums} {freqs} {types} {experiment_id} {tissue_number} />
{/if}
