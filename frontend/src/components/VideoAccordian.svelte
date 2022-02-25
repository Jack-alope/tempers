<script lang="ts">
  import { onMount } from 'svelte'
  import { Accordion, AccordionItem } from 'svelte-accessible-accordion'

  import TissueNumberSelector from './TissueNumberSelector.svelte'
  import VideoTable from './tables/VideoTable.svelte'

  import type { vid_show } from '../types/interfaces'

  let videos: vid_show

  onMount(async () => {
    await getVideos()
  })

  async function getVideos() {
    const res = await fetch(process.env.API_URL + '/videos_show', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    if (res.ok) {
      videos = await res.json()
    } else {
      return undefined
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
        <Accordion>
          {#each Object.entries(vid_list) as [date_recorded, vids]}
            <AccordionItem
              title="Date Recorded: {date_recorded}"
              class="shadow-sm rounded-lg border-2 border-blue-600 border-opacity-50"
            >
              <VideoTable bind:vids />
              <TissueNumberSelector experiment_id={exp} {date_recorded} />
            </AccordionItem>
          {/each}
        </Accordion>
        <TissueNumberSelector experiment_id={exp} />
      </AccordionItem>
    {/each}
  {/if}
</Accordion>
