<script lang="ts">
  import { onMount, onDestroy } from "svelte";
  import AddExperimet from "../components/AddExperimet.svelte";
  import AddBioReactor from "../components/AddBioReactor.svelte";
  import Modal from "../components/Modal.svelte";

  import { getBioReactors, getExperiments, getVideos } from "../apiCalls.js";

  import {
    showBioReactor,
    showExperiment,
    bio_reactors,
    experiments,
    videos,
  } from "../components/Stores.js";

  import type {
    bio_reactor_interface,
    experiment_interface,
    video_interface,
  } from "../interfaces";

  let experiments_value: experiment_interface[];
  let bio_reactors_value: bio_reactor_interface[];
  let videos_value: video_interface[];

  showExperiment.set(false);
  showBioReactor.set(false);

  const unsubscribe = bio_reactors.subscribe((value) => {
    bio_reactors_value = value;
  });

  const expunsubscribe = experiments.subscribe((value) => {
    experiments_value = value;
  });

  const vidspunsubscribe = videos.subscribe((value) => {
    videos_value = value;
  });

  onMount(async () => {
    await getBioReactors();
    await getExperiments();
    await getVideos();
  });

  async function handleBioReactorDel(id: number) {
    const res = await fetch(process.env.API_URL + `/bio_reactor/${id}`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
    });
    if (res.ok) {
      if ((await res.json()) == true) {
        bio_reactors_value = bio_reactors_value.filter(
          (bio_reactor) => bio_reactor.id !== id
        );
        $bio_reactors = bio_reactors_value;
      } else {
        alert("Cannot delete bio reactor");
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

  onDestroy(unsubscribe);
  onDestroy(expunsubscribe);
  onDestroy(vidspunsubscribe);
</script>

<div class="flex flex-wrap overflow-hidden">
  <div class="w-1/2 overflow-hidden">
    <table class="table-auto">
      <thead>
        <tr>
          <th>ID</th>
          <th>Experiment Idenifiyer</th>
          <th>Start Date</th>
          <th>Delete</th>
        </tr>
      </thead>
      <tbody>
        {#if experiments_value == undefined}
          No Experiments
        {:else}
          {#each experiments_value as experiment}
            <tr>
              <td>{experiment.id}</td>
              <td>{experiment.experiment_idenifer}</td>
              <td>{experiment.start_date}</td>
              <td
                ><button
                  class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
                  on:click={() => handleExperimentDel(experiment.id)}
                  >Delete</button
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
  </div>

  <div class="w-1/2 overflow-hidden">
    <table class="table-auto">
      <thead>
        <tr>
          <th>Id</th>
          <th>Bio Reactor Number</th>
          <th>Date Added</th>
          <th>Delete</th>
        </tr>
      </thead>
      <tbody>
        {#if bio_reactors_value === undefined}
          No Bio Reactors
        {:else}
          {#each bio_reactors_value as bio_reactor}
            <tr>
              <td>{bio_reactor.id}</td>
              <td>{bio_reactor.bio_reactor_number}</td>
              <td>{bio_reactor.date_added}</td>
              <td
                ><button
                  class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
                  on:click={() => handleBioReactorDel(bio_reactor.id)}
                  >Delete</button
                ></td
              >
            </tr>
          {/each}
        {/if}
      </tbody>
    </table>

    <button
      class="appearance-none justify-center block w-3/4 bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
      on:click={() => showBioReactor.set(true)}>Add Bio Reactor</button
    >
  </div>

  <div class="w-full overflow-hidden">
    <table class="table-auto">
      <thead>
        <tr>
          <th>Id</th>
          <th>Date Upload</th>
          <th>Date Recorded</th>
          <th>Frequency</th>
          <th>Calibration Distance</th>
          <th>Calibration Factor</th>
          <th>Experiment Idenifiyer</th>
          <th>Bio Reactor Number</th>
          <th>Delete</th>
        </tr>
      </thead>
      <tbody>
        {#if videos_value === undefined}
          No Videos
        {:else}
          {#each videos_value as video}
            <tr>
              <td>{video.id}</td>
              <td>{video.date_uploaded}</td>
              <td>{video.date_recorded}</td>
              <td>{video.frequency}</td>
              <td>{video.calibration_distance}</td>
              <td>{video.calibration_factor}</td>
              <td>{video.experiment_idenifer}</td>
              <td>{video.bio_reactor_number}</td>
              <td
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
  </div>

  <div class="w-full overflow-hidden">
    <!-- Column Content -->
  </div>
</div>

{#if $showExperiment}
  <Modal on:close={() => showExperiment.set(false)}>
    <h1 slot="header">Add a Experiment</h1>
    <p slot="content">
      <AddExperimet />
    </p>
  </Modal>
{:else if $showBioReactor}
  <Modal on:close={() => showBioReactor.set(false)}>
    <h1 slot="header">Add a Bio Reactor</h1>
    <p slot="content">
      <AddBioReactor />
    </p>
  </Modal>
{/if}
