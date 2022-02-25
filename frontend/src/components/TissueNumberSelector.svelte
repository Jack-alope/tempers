<script lang="ts">
  import { onMount } from 'svelte'

  export let experiment_id: string
  export let date_recorded: string = null

  let selectedTissueNumber: number
  let tissue_numbers

  onMount(async () => {
    await getTissueNumbers()
  })

  async function getTissueNumbers() {
    let url
    if (date_recorded) {
      url =
        process.env.API_URL +
        `/tissues_in_experiment_by_date_recorded?experiment_id=${experiment_id}&date_recorded=${date_recorded}`
    } else {
      url = process.env.API_URL + `/tissues_in_experiment?experiment_id=${experiment_id}`
    }
    const res = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    if (res.ok) {
      tissue_numbers = await res.json()
    } else {
      return undefined
    }
  }

  async function handleTissueNumberSubmitted() {
    if (date_recorded) {
      window.location.href = `/analyze?experiment_id=${experiment_id}&tissue_number=${selectedTissueNumber}&date_recorded=${date_recorded}`
    } else {
      window.location.href = `/analyze?experiment_id=${experiment_id}&tissue_number=${selectedTissueNumber}`
    }
  }
</script>

{#if !tissue_numbers}
  <h1>no tissues</h1>
{:else}
  {#if date_recorded}
    <p>
      To analyze by tissue number within an experiment recorded on {date_recorded}
      select tissue number
    </p>
  {:else}
    <p>To analyze by tissue number within an experiment select tissue number</p>
  {/if}

  <form on:submit|preventDefault={handleTissueNumberSubmitted}>
    <select bind:value={selectedTissueNumber}>
      {#each tissue_numbers as tissue_number}
        <option value={tissue_number}>
          {tissue_number}
        </option>
      {/each}
    </select>

    <button type="submit"> Submit </button>
  </form>
{/if}
