<script lang="ts">
  import AddExperimet from "../components/AddExperimet.svelte";
  import AddBioReactor from "../components/AddBioReactor.svelte";
  import Modal from "../components/Modal.svelte";

  import {
    showBioReactor,
    showExperiment,
    downloadModal,
  } from "../components/Stores.js";

  import ExperimentTable from "../components/tables/ExperimentTable.svelte";
  import BioReactorTable from "../components/tables/BioReactorTable.svelte";
  import VideoTable from "../components/tables/VideoTable.svelte";

  showExperiment.set(false);
  showBioReactor.set(false);
</script>

<div class="flex flex-wrap overflow-hidden">
  <div class="w-1/2 overflow-hidden">
    <ExperimentTable />
  </div>

  <div class="w-1/2 overflow-hidden">
    <BioReactorTable />
  </div>

  <div class="w-full overflow-hidden">
    <VideoTable />
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
{:else if $downloadModal}
  <!-- REVIEW: this is ugly -->
  <Modal on:close={() => ($downloadModal = false)}>
    <h1 slot="header">Download experiment</h1>
    <p slot="content">Downloading....</p>
  </Modal>
{/if}
