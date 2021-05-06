<script lang="ts">
  import { onMount, onDestroy } from "svelte";
  import { getVideos } from "../../apiCalls.js";
  import { videos } from "../../components/Stores.js";
  import type { video_interface } from "../../interfaces";

  onMount(async () => {
    await getVideos();
  });

  let videos_value: video_interface[];

  const vidspunsubscribe = videos.subscribe((value) => {
    videos_value = value;
  });

  async function handleVideoDel(id: number) {
    const res = await fetch(process.env.API_URL + `/video/${id}`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
    });
    if (res.ok) {
      videos_value = videos_value.filter((video) => video.id !== id);
      $videos = videos_value;
    } else {
      alert("Something went wrong");
    }
  }

  onDestroy(vidspunsubscribe);
</script>

<table class="table-auto min-w-full divide-y divide-gray-200">
  <thead class="bg-gray-50">
    <tr>
      <th
        scope="col"
        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
        >Id</th
      >
      <th
        scope="col"
        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
        >Date Upload</th
      >
      <th
        scope="col"
        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
        >Date Recorded</th
      >
      <th
        scope="col"
        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
        >Frequency</th
      >
      <th
        scope="col"
        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
        >Calibration Distance</th
      >
      <th
        scope="col"
        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
        >Calibration Factor</th
      >
      <th
        scope="col"
        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
        >Experiment Idenifiyer</th
      >
      <th
        scope="col"
        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
        >Bio Reactor Number</th
      >
      <th
        scope="col"
        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
        >Delete</th
      >
    </tr>
  </thead>
  <tbody class="bg-white divide-y divide-gray-200">
    {#if !videos_value}
      No Videos
    {:else}
      {#each videos_value as video}
        <tr>
          <td class="px-6 py-4 whitespace-nowrap">{video.id}</td>
          <td class="px-6 py-4 whitespace-nowrap">{video.date_uploaded}</td>
          <td class="px-6 py-4 whitespace-nowrap">{video.date_recorded}</td>
          <td class="px-6 py-4 whitespace-nowrap">{video.frequency}</td>
          <td class="px-6 py-4 whitespace-nowrap"
            >{video.calibration_distance}</td
          >
          <td class="px-6 py-4 whitespace-nowrap">{video.calibration_factor}</td
          >
          <td class="px-6 py-4 whitespace-nowrap"
            >{video.experiment_idenifer}</td
          >
          <td class="px-6 py-4 whitespace-nowrap">{video.bio_reactor_number}</td
          >
          <td class="px-6 py-4 whitespace-nowrap"
            ><button
              class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
              on:click={() => handleVideoDel(video.id)}>Delete</button
            ></td
          >
        </tr>
      {/each}
    {/if}
  </tbody>
</table>
