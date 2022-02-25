<script lang="ts">
  import { onMount } from "svelte";
  import { getExperiments } from "../../apiCalls.js";
  import Modal from "../../components/Modal.svelte";
  import AddExperimet from "../../components/AddExperimet.svelte";
  import UploadExperimentArchive from "../../components/UploadExperimentArchive.svelte";
  import { experiments } from "../../components/Stores.js";
  import DownloadModal from "../DownloadModal.svelte"

  let uploadArchive = false;
  let showDownloadModal = false;
  let showExperiment =false;

  onMount(async () => {
    await getExperiments();
  });


  async function handleExperimentDownload(id: number) {
    showDownloadModal = true;
    const res = await fetch(process.env.API_URL + `/experimentsJSON/${id}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });
    if (res.ok) {
      const file = await res.blob();
      if (file) {
        const blob = new Blob([file]);
        saveAs(blob, `${id}.zip`);
        showDownloadModal = false;
      }
    } else {
      alert("Something went wrong");
    }
  }

  async function handleExperimentDel(id: number) {
    const res = await fetch(process.env.API_URL + `/experiment/${id}`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
    });
    if (res.ok) {
      if ((await res.json()) == true) {
        $experiments = $experiments.filter(
          (experiment) => experiment.id !== id
        );
      } else {
        alert("Cannot delete Experiment");
      }
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
        >Experiment ID</th
      >
      <th
        scope="col"
        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
        >Start Date</th
      >
      <th
        scope="col"
        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
        >Download</th
      >
      <th
        scope="col"
        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
        >Delete</th
      >
    </tr>
  </thead>
  <tbody class="bg-white divide-y divide-gray-200">
    {#if !$experiments}
      No Experiments
    {:else}
      {#each $experiments as experiment}
        <tr>
          <td class="px-6 py-4 whitespace-nowrap">{experiment.id}</td>
          <td class="px-6 py-4 whitespace-nowrap">{experiment.start_date}</td>
          <td class="px-6 py-4 whitespace-nowrap">
            <button
              class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
              on:click={() => handleExperimentDownload(experiment.id)}
              >Download</button
            >
          </td>
          <td class="px-6 py-4 whitespace-nowrap"
            ><button
              class="{experiment.has_vids
                ? 'bg-gray-300'
                : 'bg-red-500 hover:bg-red-700'} text-white font-bold py-2 px-4 rounded"
              disabled={experiment.has_vids}
              title={experiment.has_vids
                ? "Cannot Delete Must Delete Videos First"
                : "Delete"}
              on:click={() => handleExperimentDel(experiment.id)}>Delete</button
            ></td
          >
        </tr>
      {/each}
    {/if}
  </tbody>
</table>

<div class="flex flex-wrap overflow-hidden">
  <div class="w-1/2 overflow-hidden">
    <button
      class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
      on:click={() => (showExperiment = true)}>Add Experiment</button
    >
  </div>
  <div class="w-1/2 overflow-hidden">
    <button
      class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
      on:click={() => (uploadArchive = true)}>Upload Archive</button
    >
  </div>
</div>

{#if uploadArchive}
  <Modal on:close={() => (uploadArchive = false)}>
    <h1 slot="header">Upload Archive</h1>
    <p slot="content">
      <UploadExperimentArchive bind:uploadArchive />
    </p>
  </Modal>
{:else if showDownloadModal}
  <DownloadModal bind:showDownloadModal />
{:else if showExperiment}
  <Modal on:close={() => (showExperiment = false)}>
    <h1 slot="header">Add a Experiment</h1>
    <p slot="content">
      <AddExperimet bind:showExperiment on:updateExps={async () => getExperiments()}/>
    </p>
  </Modal>
{/if}

<style>
</style>
