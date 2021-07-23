<script lang="ts">
  import { onMount } from "svelte";
  import Modal from "../../components/Modal.svelte";
  import { getBioReactors } from "../../apiCalls.js";
  import { showBioReactor, bio_reactors } from "../../components/Stores.js";
  import AddBioReactor from "../../components/AddBioReactor.svelte";

  onMount(async () => {
    await getBioReactors();
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
        $bio_reactors = $bio_reactors.filter(
          (bio_reactor) => bio_reactor.id !== id
        );
        $bio_reactors = $bio_reactors;
      } else {
        alert("Cannot delete bio reactor");
      }
    } else {
      alert("Something went wrong");
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
        >Post Distance</th
      >
      <th
        scope="col"
        class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
        >Youngs Modulus</th
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
            >{bio_reactor.post_distance}</td
          >
          <td class="px-6 py-4 whitespace-nowrap"
            >{bio_reactor.youngs_modulus}</td
          >
          <td class="px-6 py-4 whitespace-nowrap">{bio_reactor.date_added}</td>
          <td class="px-6 py-4 whitespace-nowrap"
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
  on:click={() => ($showBioReactor = true)}>Add Bio Reactor</button
>

{#if $showBioReactor}
  <Modal on:close={() => ($showBioReactor = false)}>
    <h1 slot="header">Add a Bio Reactor</h1>
    <p slot="content">
      <AddBioReactor />
    </p>
  </Modal>
{/if}
