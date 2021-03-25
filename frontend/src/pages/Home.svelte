<script lang="ts">
  import AddExperimet from "../componets/AddExperimet.svelte";
  import AddBioReactor from "../componets/AddBioReactor.svelte";
  import Modal from "../componets/Modal.svelte";

  let showExperiment = false;
  let showBioReactor = false;

  async function handleExperimentSubmitted(event) {
    const experimentInfo = event.detail.experimentInfo;
    const res = await fetch(process.env.url + "/addExperiment", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(experimentInfo),
    });

    if (res.ok) {
      window.location.replace("/tracking");
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
      window.location.replace("/tracking");
    } else {
      alert("Something went wrong");
    }
  }
</script>

<h1 class="text-red-800 text-3xl font-bold p-3">Hello World!</h1>

<button
  class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
  on:click={() => (showExperiment = true)}>Add Experiment</button
>

<button
  class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
  on:click={() => (showBioReactor = true)}>Add Bio Reactor</button
>

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
