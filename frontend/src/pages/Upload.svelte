<script lang="ts">
  import { createForm } from "svelte-forms-lib";

  let files;

  async function addVid(values) {
    const formData = new FormData();
    formData.append("info", JSON.stringify(values));
    formData.append("file", files[0]);
    console.log(formData);

    console.log(files);
    const res = await fetch(process.env.url + "/upload", {
      method: "POST",
      body: formData,
    });

    if (res.ok) {
      window.location.replace("/tracking");
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
          post_number: "",
          tissue_number: "",
          tissue_type: "",
        },
      ],

      frequency: "",
    },
    onSubmit: (values) => {
      addVid(values);
    },
  });

  const add = () => {
    $form.tissues = $form.tissues.concat({
      post_number: "",
      tissue_number: "",
      tissue_type: "",
    });
    // $errors.tissues = $tissues.tissues.concat({ name: "", email: "" });
  };

  const remove = (i) => () => {
    $form.tissues = $form.tissues.filter((u, j) => j !== i);
    // $errors.tissues = $errors.tissues.filter((u, j) => j !== i);
  };
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
      />
    </div>

    <div class="w-full md:w-1/3 px-3">
      <label
        class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
        for="bio_reactor_id">Bio Reactor</label
      >
      <input
        type="number"
        id="bio_reactor_id"
        name="bio_reactor_id"
        class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
        bind:value={$form.bio_reactor_id}
      />
    </div>

    <div class="w-full md:w-1/3 px-3">
      <label
        class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
        for="experiment_id">Experiment Number</label
      >
      <input
        type="text"
        id="experiment_id"
        name="experiment_id"
        class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
        bind:value={$form.experiment_id}
      />
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
            <input
              name={`tissues[${j}].post_number`}
              placeholder="Post Number"
              on:change={handleChange}
              on:blur={handleChange}
              class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
              bind:value={$form.tissues[j].post_number}
            />
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
      <input
        class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
        type="submit"
      />
    </div>
  </div>
</form>
