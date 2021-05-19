<script lang="ts">
  import { onMount } from "svelte";
  import Grapher from "../components/Grapher.svelte";

  import { json_data_list } from "../components/Stores.js";

  let video_id: number;

  let nums, freqs, types;

  async function handleVideoSelected(video_id: number) {
    const res = await fetch(
      process.env.API_URL + `/analyze?video_id=${video_id}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      }
    );

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
    await handleVideoSelected(video_id);
  });
</script>

<svelte:head>
  <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
  <script
    src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"
    type="text/javascript">
  </script>
</svelte:head>

<h1>Analysis</h1>

{#if nums && freqs && types && video_id}
  <Grapher {nums} {freqs} {types} {video_id} />
{/if}
