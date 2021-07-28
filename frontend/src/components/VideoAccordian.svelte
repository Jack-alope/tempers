<script lang="ts">
  import { onMount } from "svelte";
  import { Accordion, AccordionItem } from "svelte-accessible-accordion";

  import VideoTable from "./tables/VideoTable.svelte";
  import type { vid_show } from "../interfaces";

  let videos: vid_show;

  onMount(async () => {
    await getVideos();
  });

  async function getVideos() {
    const res = await fetch(process.env.API_URL + "/videos_show", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });
    if (res.ok) {
      videos = await res.json();
    } else {
      return undefined;
    }
  }
</script>

<Accordion>
  {#if videos}
    {#each Object.entries(videos) as [exp, vid_list]}
      <AccordionItem
        title="experiment: {exp}"
        class="shadow-sm rounded-lg border-2 border-blue-600 border-opacity-50"
      >
        <VideoTable videos={vid_list} experiment_ident={exp} />
      </AccordionItem>
    {/each}
  {/if}
</Accordion>
