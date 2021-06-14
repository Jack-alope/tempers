<script lang="ts">
  import ExperimentTable from "../components/tables/ExperimentTable.svelte";
  import BioReactorTable from "../components/tables/BioReactorTable.svelte";
  import VideoAccordian from "../components/VideoAccordian.svelte";
</script>

<div class="flex flex-wrap overflow-hidden">
  <div class="w-1/2 py-4 px-4 overflow-hidden shadow-lg">
    <h1
      class="text-2xl text-center font-bold leading-7 text-gray-700 sm:text-3xl sm:truncate"
    >
      Experiments
    </h1>
    <ExperimentTable />
  </div>

  <div class="w-1/2 py-4 px-4 overflow-hidden shadow-lg">
    <h1
      class="text-2xl text-center font-bold leading-7 text-gray-700 sm:text-3xl sm:truncate"
    >
      Bio Reactors
    </h1>
    <BioReactorTable />
  </div>

  <div class="w-full py-4 px-4 overflow-hidden shadow-lg">
    <h1
      class="text-2xl text-center font-bold leading-7 text-gray-700 sm:text-3xl sm:truncate"
    >
      Videos
    </h1>
    <VideoAccordian />
  </div>
</div>
