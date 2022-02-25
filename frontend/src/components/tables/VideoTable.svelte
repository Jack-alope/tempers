<script lang="ts">
  import type { vid_date_show } from "../../types/interfaces"

  export let vids : vid_date_show[];

  async function handleVideoDel(id: number) {
    const res = await fetch(process.env.API_URL + `/video/${id}`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
    });
    if (res.ok) {
      vids = vids.filter((video) => video.id !== id);
      console.log("deleted")
    } else {
      alert("Something went wrong");
    }
  }
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
        >Note</th
      >
      <th
        scope="col"
        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
        >Bio Reactor Number</th
      >
      <th
        scope="col"
        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
        >Track</th
      >
      <th
        scope="col"
        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
        >Analyse</th
      >

      <th
        scope="col"
        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
        >Delete</th
      >
    </tr>
  </thead>

  <tbody class="bg-white divide-y divide-gray-200">
      {#each vids as video}
        <tr>
          <td class="px-6 py-4 whitespace-nowrap">{video.id}</td>
          <td class="px-6 py-4 whitespace-nowrap">{video.date_recorded}</td>
          <td class="px-6 py-4 whitespace-nowrap">{video.frequency}</td>
          <td class="px-6 py-4 whitespace-nowrap"
            >{#if video.video_note}{video.video_note}{/if}</td
          >
          <td class="px-6 py-4 whitespace-nowrap">{video.bio_reactor_number}</td
          >
          <td class="px-6 py-4 whitespace-nowrap">
            <button
              class="{video.save_location
                ? 'bg-green-500 hover:bg-green-300'
                : 'bg-gray-300'}  text-white font-bold py-2 px-4 rounded"
              disabled={!video.save_location}
              title={video.save_location ? null : "No Video To Track"}
              on:click={() =>
                (window.location.href = `/tracking?video_id=${video.id}`)}
              >Track</button
            >
          </td>
          <td class="px-6 py-4 whitespace-nowrap"
            ><button
              class="{video.tracked
                ? 'bg-green-500 hover:bg-green-600'
                : 'bg-gray-300'}  text-white font-bold py-2 px-4 rounded"
              disabled={!video.tracked}
              title={video.tracked ? null : "Must Track First"}
              on:click={() =>
                (window.location.href = `/analyze?video_id=${video.id}`)}
              >Analyse</button
            ></td
          >
          <td class="px-6 py-4 whitespace-nowrap"
            ><button
              class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
              on:click={() => handleVideoDel(video.id)}>Delete</button
            ></td
          >
        </tr>
      {/each}
  </tbody>
</table>
