  <script lang="ts">
      import Modal from "./Modal.svelte";
      export let showDownloadModal: boolean = false;
  </script>
  
  
  <!-- REVIEW: this is ugly --> 
<Modal on:close={() => (showDownloadModal = false)}>
    <h1 slot="header">Download experiment</h1>
    <p slot="content">Downloading....</p>
</Modal>