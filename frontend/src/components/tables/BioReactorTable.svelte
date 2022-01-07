<script lang="ts">
  import { onMount } from "svelte";
  import Modal from "../../components/Modal.svelte";
  import { getBioReactors } from "../../apiCalls.js";
  import { showBioReactor, bio_reactors } from "../../components/Stores.js";
  import AddBioReactor from "../../components/AddBioReactor.svelte";
  import DownloadModal from "../DownloadModal.svelte";
  import UploadBioReactorArchive from "../UploadBioReactorArchive.svelte";


  onMount(async () => {
    await getBioReactors();
  });

  let showDownloadModal: boolean = false;
  let uploadBioReactorArchive: boolean = false;

  async function handleBioReactorDel(id: number) {
    const res = await fetch(process.env.API_URL + `/bio_reactor/${id}`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
    });
    if (res.ok) {
      if ((await res.json()) == true) {
        $bio_reactors = $bio_reactors.filter(
          (bio_reactor) => bio_reactor.id !== id
        );
      } else {
        alert("Cannot delete bio reactor");
      }
    } else {
      alert("Something went wrong");
    }
  }

  async function handleDownloadBioReactor(){
    showDownloadModal = true;
    const res = await fetch(process.env.API_URL + "/download/bio_reactor_archive", {
      method: "GET",
      headers: {
        "Content-Type": "application/json"
      },

    });

    if (res.ok){
      const file = await res.blob();
      if (file) {
        const date = new Date().toISOString().split('T')[0];
        const blob = new Blob([file]);
        saveAs(blob, `bio_reactors_archive_${date}.json`);
        showDownloadModal = false;
      }
    } else {
      alert("Something Went Wrong")
    }
  }
</script>

<table class="table-auto min-w-full divide-y divide-grey-200">
  <thead class="bg-grey-50">
    <tr>
      <th
        scope="col"
        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
        >Id</th
      >
      <th
        scope="col"
        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
        >Bio Reactor Number</th
      >
      <th
        scope="col"
        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
        >Note</th
      >
      <th
        scope="col"
        class="px-6 py-3 text-left text-xs font-medium text-gray-500 tracking-wider"
        >POST DISTANCE (mm)</th
      >
      <th
        scope="col"
        class="px-6 py-3 text-left text-xs font-medium text-gray-500 tracking-wider"
        >YOUNGS MODULUS (MPa)</th
      >
      <th
        scope="col"
        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
        >Date Added</th
      >
      <th
        scope="col"
        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
        >Delete</th
      >
    </tr>
  </thead>
  <tbody class="bg-white divide-y divide-gray-200">
    {#if !$bio_reactors}
      No Bio Reactors
    {:else}
      {#each $bio_reactors as bio_reactor}
        <tr>
          <td class="px-6 py-4 whitespace-nowrap">{bio_reactor.id}</td>
          <td class="px-6 py-4 whitespace-nowrap"
            >{bio_reactor.bio_reactor_number}</td
          >
          <td class="px-6 py-4 whitespace-nowrap"
            >{#if bio_reactor.bio_reactor_note}{bio_reactor.bio_reactor_note}{/if}</td
          >
          <td class="px-6 py-4 whitespace-nowrap"
            >{bio_reactor.post_distance}</td
          >
          <td class="px-6 py-4 whitespace-nowrap"
            >{bio_reactor.youngs_modulus}</td
          >
          <td class="px-6 py-4 whitespace-nowrap">{bio_reactor.date_added}</td>
          <td class="px-6 py-4 whitespace-nowrap"
            ><button
              class="{bio_reactor.has_vids
                ? 'bg-gray-300'
                : 'bg-red-500 hover:bg-red-700'} text-white font-bold py-2 px-4 rounded"
              disabled={bio_reactor.has_vids}
              title={bio_reactor.has_vids
                ? "Cannot Delete Must Delete Videos First"
                : "Delete"}
              on:click={() => handleBioReactorDel(bio_reactor.id)}
              >Delete</button
            ></td
          >
        </tr>
      {/each}
    {/if}
  </tbody>
</table>
<div class="flex flex-wrap overflow-hidden">
  <div class="w-1/3 overflow-hidden">
    <button
    class="appearance-none justify-center block w-3/4 bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
    on:click={() => ($showBioReactor = true)}>Add Bio Reactor</button
  >
  </div>
  <div class="w-1/3 overflow-hidden">
    <button
      class="{$bio_reactors 
      ? "bg-blue-500 hover:bg-blue-700 text-white"
      :"bg-gray-200 text-gray-700"} 
      appearance-none justify-center block w-3/4 bg-gray-200 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
      on:click={() =>(handleDownloadBioReactor())}>Download Bio Reactors</button>
  </div>
  <div class="w-1/3 overflow-hidden">
    <button
    class="appearance-none justify-center block w-3/4 bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
    on:click={() => (uploadBioReactorArchive = true)}>Upload Bio Reactor Archive</button
  >

  </div>
</div>

{#if $showBioReactor}
  <Modal on:close={() => ($showBioReactor = false)}>
    <h1 slot="header">Add a Bio Reactor</h1>
    <p slot="content">
      <AddBioReactor />
    </p>
  </Modal>
{:else if showDownloadModal}
  <DownloadModal bind:showDownloadModal />
{:else if uploadBioReactorArchive}
<Modal on:close={() => (uploadBioReactorArchive = false)}>
  <h1 slot="header">Upload Archive</h1>
  <p slot="content">
    <UploadBioReactorArchive bind:uploadBioReactorArchive />
  </p>
</Modal>
{/if}
