<script lang="ts">
  import { onMount, onDestroy } from "svelte";
  import { getExperiments } from "../../apiCalls.js";
  import {
    showExperiment,
    experiments,
    downloadModal,
  } from "../../components/Stores.js";

  import type { experiment_interface } from "../../interfaces";

  let experiments_value: experiment_interface[];

  const expunsubscribe = experiments.subscribe((value) => {
    experiments_value = value;
  });

  onMount(async () => {
    await getExperiments();
  });

  async function handleExperimentDownload(id: number) {
    $downloadModal = true;
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
        $downloadModal = false;
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
        experiments_value = experiments_value.filter(
          (experiment) => experiment.id !== id
        );
        $experiments = experiments_value;
      } else {
        alert("Cannot delete Experimet");
      }
    } else {
      alert("Something went wrong");
    }
  }

  onDestroy(expunsubscribe);
</script>

<table class="table-auto min-w-full divide-y divide-gray-200">
  <thead class="bg-gray-50">
    <tr>
      <th
        scope="col"
        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
        >ID</th
      >
      <th
        scope="col"
        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
        >Experiment Idenifiyer</th
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
    {#if !experiments_value}
      No Experiments
    {:else}
      {#each experiments_value as experiment}
        <tr>
          <td class="px-6 py-4 whitespace-nowrap">{experiment.id}</td>
          <td class="px-6 py-4 whitespace-nowrap"
            >{experiment.experiment_idenifer}</td
          >
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
              class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
              on:click={() => handleExperimentDel(experiment.id)}>Delete</button
            ></td
          >
        </tr>
      {/each}
    {/if}
  </tbody>
</table>

<button
  class="appearance-none block w-3/4 bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
  on:click={() => showExperiment.set(true)}>Add Experiment</button
>

<style>
</style>
