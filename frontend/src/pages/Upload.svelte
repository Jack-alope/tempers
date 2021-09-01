<script lang="ts">
  import { onDestroy, onMount } from "svelte";
  import { createForm } from "svelte-forms-lib";
  // import * as yup from "yup";
  import {
    getBioReactors,
    getExperiments,
    getPostOptions,
  } from "../apiCalls.js";
  import { bio_reactors, experiments } from "../components/Stores.js";
  import type {
    bio_reactor_interface,
    experiment_interface,
    post_interface,
  } from "../interfaces";

  let files;
  let experiments_value: experiment_interface[];
  let bio_reactors_value: bio_reactor_interface[];
  let post_options: post_interface[];

  const unsubscribe = bio_reactors.subscribe((value) => {
    bio_reactors_value = value;
  });

  const expunsubscribe = experiments.subscribe((value) => {
    experiments_value = value;
  });

  onMount(async () => {
    await getBioReactors();
    await getExperiments();
  });

  async function addVid(values) {
    const formData = new FormData();
    formData.append("info", JSON.stringify(values));
    formData.append("file", files[0]);

    const res = await fetch(process.env.API_URL + "/upload", {
      method: "POST",
      body: formData,
    });

    if (res.ok) {
      window.location.replace("/database");
    } else {
      alert("Something went wrong");
    }
  }
  // TODO: add form validations
  const { form, errors, state, handleChange, handleSubmit } = createForm({
    initialValues: {
      date_recorded: "",
      bio_reactor_id: "",
      experiment_id: "",

      tissues: [
        {
          post_id: "",
          tissue_number: "",
          tissue_type: "",
        },
      ],

      frequency: "",
      video_note: "",
    },
    /*
    TODO: figure out validation lo dash error
    validationSchema: yup.object().shape({
      date_recorded: yup.date().required(),
      bio_reactor_id: yup.number().required(),
      experiment_id: yup.number().required(),
    }),
    */
    onSubmit: (values) => {
      addVid(values);
    },
  });

  const add = () => {
    $form.tissues = $form.tissues.concat({
      post_id: "",
      tissue_number: "",
      tissue_type: "",
    });
    // $errors.tissues = $tissues.tissues.concat({ name: "", email: "" });
  };

  const remove = (i) => () => {
    $form.tissues = $form.tissues.filter((u, j) => j !== i);
    // $errors.tissues = $errors.tissues.filter((u, j) => j !== i);
  };

  async function handleBioChange() {
    post_options = await getPostOptions($form.bio_reactor_id);
  }

  onDestroy(unsubscribe);
  onDestroy(expunsubscribe);
</script>

<form class="w-full" on:submit={handleSubmit}>
  <!-- TODO: Maybe use grid instead -->
  <div class="flex flex-wrap py-5">
    <div class="w-full md:w-1/3 px-3">
      <label
        class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
        for="date_recorded">Date Recorded</label
      >
      <input
        type="date"
        id="date_recorded"
        name="date_recorded"
        class="appearance-none block w-full bg-gray-200 text-gray-700 border border-red-500 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white"
        bind:value={$form.date_recorded}
        on:change={handleChange}
      />
    </div>

    <div class="w-full md:w-1/3 px-3">
      <label
        class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
        for="bio_reactor_id">Bio Reactor</label
      >
      <select
        id="bio_reactor_id"
        name="bio_reactor_id"
        class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
        bind:value={$form.bio_reactor_id}
        on:blur={handleBioChange}
      >
        <option />
        {#if bio_reactors_value == undefined}
          <option>NA</option>>
        {:else}
          {#each bio_reactors_value as bio_reactor}
            <option value={bio_reactor.id}
              >{bio_reactor.bio_reactor_number}</option
            >
          {/each}
        {/if}
      </select>
    </div>

    <div class="w-full md:w-1/3 px-3">
      <label
        class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
        for="experiment_id">Experiment Number</label
      >
      <select
        id="experiment_id"
        name="experiment_id"
        class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
        bind:value={$form.experiment_id}
      >
        <option />
        {#if experiments_value == undefined}
          <option>NA</option>>
        {:else}
          {#each experiments_value as experiment}
            <option value={experiment.id}
              >{experiment.id} - Start Date: {experiment.start_date}</option
            >
          {/each}
        {/if}
      </select>
    </div>
    <div class="w-full px-3 py-5">
      <h1
        class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
      >
        Add Tissues
      </h1>

      {#each $form.tissues as tissue, j}
        <div class="flex flex-wrap py-3">
          <div class="w-full md:w-1/4 px-3">
            <select
              name={tissue.post_id}
              placeholder="Post Number"
              on:blur={handleChange}
              class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
              bind:value={$form.tissues[j].post_id}
            >
              <option />
              {#if post_options == undefined}
                <option>NA</option>
              {:else}
                {#each post_options as post}
                  <option value={post.id}>{post.post_number}</option>
                {/each}
              {/if}
            </select>
          </div>

          <div class="w-full md:w-1/4 px-3">
            <input
              placeholder="Tissue Number"
              name={`tissues[${j}].tissue_number`}
              on:change={handleChange}
              on:blur={handleChange}
              class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
              bind:value={$form.tissues[j].tissue_number}
            />
          </div>

          <div class="w-full md:w-1/4 px-3">
            <input
              placeholder="Tissue Type"
              name={`tissues[${j}].tissue_type`}
              on:change={handleChange}
              on:blur={handleChange}
              class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
              bind:value={$form.tissues[j].tissue_type}
            />
          </div>

          <div class="w-full md:w-1/4 px-3">
            {#if $form.tissues.length !== 1}
              <button
                class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
                type="button"
                on:click={remove(j)}>-</button
              >
            {/if}

            {#if j === $form.tissues.length - 1}
              <button
                class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                type="button"
                on:click={add}>+</button
              >
            {/if}
          </div>
        </div>
      {/each}
    </div>

    <div class="w-full md:w-1/2 px-3">
      <label
        class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
        for="frequency">Frequency:</label
      >
      <input
        type="number"
        id="frequency"
        name="frequency"
        placeholder="frequency"
        step="any"
        class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
        bind:value={$form.frequency}
      />
    </div>

    <div class="w-full md:w-1/2 px-3">
      <label
        class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
        for="vid">Upload Video</label
      >
      <input
        class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
        id="vid"
        name="vid"
        type="file"
        bind:files
      />
    </div>

    <div class="w-1/2 px-3 py-3">
      <label
        class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
        for="vid">Video Note</label
      >
      <input
        class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
        type="text"
        id="video_note"
        name="video_note"
        bind:value={$form.video_note}
      />
    </div>

    <div class="w-1/2 px-3 py-5">
      <input
        class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
        type="submit"
      />
    </div>
  </div>
</form>
