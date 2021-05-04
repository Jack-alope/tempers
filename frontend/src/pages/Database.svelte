<script lang="ts">
  import ExperimentTable from "../components/tables/ExperimentTable.svelte";
  import BioReactorTable from "../components/tables/BioReactorTable.svelte";
  import VideoTable from "../components/tables/VideoTable.svelte";
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
