<script lang="ts">
  import { onMount } from "svelte";
  import AddExperimet from "../components/AddExperimet.svelte";
  import AddBioReactor from "../components/AddBioReactor.svelte";
  import Modal from "../components/Modal.svelte";

  let showExperiment = false;
  let showBioReactor = false;

  interface experiment {
    id: number;
    experiment_idenifer: string;
    start_date: Date;
  }

  interface bio_reactor {
    id: number;
    bio_reactor_number: number;
    date_added: Date;
  }

  let experiments: experiment[];
  let bio_reactors: bio_reactor[];

  onMount(async () => {
    bio_reactors = await getBioReactors();
    experiments = await getExperiments();
  });

  async function getBioReactors() {
    const res = await fetch(process.env.url + "/bio_reactors", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });
    if (res.ok) {
      return await res.json();
    } else {
    }
  }

  async function getExperiments() {
    const res = await fetch(process.env.url + "/experiments", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });
    if (res.ok) {
      return await res.json();
    } else {
    }
  }

  async function handleBioReactorDel(id: number) {
    const res = await fetch(process.env.url + `/bio_reactor/${id}`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
    });
    if (res.ok) {
      bio_reactors = bio_reactors.filter(
        (bio_reactor) => bio_reactor.id !== id
      );
    } else {
      alert("Something went wrong");
    }
  }

  async function handleExperimentDel(id: number) {
    const res = await fetch(process.env.url + `/experiment/${id}`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
    });
    if (res.ok) {
      experiments = experiments.filter((experiment) => experiment.id !== id);
    } else {
      alert("Something went wrong");
    }
  }

  async function handleExperimentSubmitted(event) {
    const experimentInfo = event.detail.experimentInfo;
    console.log(experimentInfo);
    const res = await fetch(process.env.url + "/addExperiment", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(experimentInfo),
    });

    if (res.ok) {
      showExperiment = false;
      // REVIEW: try to emit and avoid extra call
      experiments = await getExperiments();
    } else {
      alert("Something went wrong");
    }
  }

  async function handleBioReactorSubmitted(event) {
    const bio_reactor_info = event.detail.bioReactorInfo;
    console.log(bio_reactor_info);
    const res = await fetch(process.env.url + "/addBioReactor", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(bio_reactor_info),
    });

    if (res.ok) {
      showBioReactor = false;
      // REVIEW: try to emit and avoid extra call
      bio_reactors = await getBioReactors();
    } else {
      alert("Something went wrong");
    }
  }
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
        {#if experiments === undefined}
          No Experiments
        {:else}
          {#each experiments as experiment}
            <tr>
              <td>{experiment.id}</td>
              <td>{experiment.experiment_idenifer}</td>
              <td>{experiment.start_date}</td>
              <td
                ><button on:click={() => handleExperimentDel(experiment.id)}
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
      on:click={() => (showExperiment = true)}>Add Experiment</button
    >
  </div>

  <div class="w-1/2 overflow-hidden">
    <table class="table-auto">
      <thead>
        <tr>
          <th>Id</th>
          <th>Bio Reactor Number</th>
          <th>Datem Added</th>
          <th>Delete</th>
        </tr>
      </thead>
      <tbody>
        {#if bio_reactors === undefined}
          No Bio Reactors
        {:else}
          {#each bio_reactors as bio_reactor}
            <tr>
              <td>{bio_reactor.id}</td>
              <td>{bio_reactor.bio_reactor_number}</td>
              <td>{bio_reactor.date_added}</td>
              <td
                ><button on:click={() => handleBioReactorDel(bio_reactor.id)}
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
      on:click={() => (showBioReactor = true)}>Add Bio Reactor</button
    >
  </div>

  <div class="w-full overflow-hidden">
    <!-- Column Content -->
  </div>

  <div class="w-full overflow-hidden">
    <!-- Column Content -->
  </div>
</div>

{#if showExperiment}
  <Modal on:close={() => (showExperiment = false)}>
    <h1 slot="header">Add a Experiment</h1>
    <p slot="content">
      <AddExperimet on:submitted={handleExperimentSubmitted} />
    </p>
  </Modal>
{:else if showBioReactor}
  <Modal on:close={() => (showBioReactor = false)}>
    <h1 slot="header">Add a Bio Reactor</h1>
    <p slot="content">
      <AddBioReactor on:submitted={handleBioReactorSubmitted} />
    </p>
  </Modal>
{/if}
