<script lang="ts">
  import SelectVideo from "../components/SelectVideo.svelte";
  import Grapher from "../components/Grapher.svelte";

  import { video_id, json_data_list } from "../components/Stores.js";

  let vidSelected = false;

  let video_id_value: number;
  let nums, freqs, types;

  video_id.subscribe((value) => {
    video_id_value = value;
  });

  async function handleVideoSelected() {
    const res = await fetch(
      process.env.API_URL + `/analyze?video_id=${video_id_value}`,
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

      vidSelected = true;
    } else {
      alert("Something went wrong");
    }
  }
</script>

<svelte:head>
  <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
  <script
    src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"
    type="text/javascript">
  </script>
</svelte:head>

<h1>Analysis</h1>

{#if !vidSelected}
  <SelectVideo on:video_selected={handleVideoSelected} />
{:else}
  <Grapher {nums} {freqs} {types} />
{/if}
