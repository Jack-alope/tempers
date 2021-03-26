<script lang="ts">
  import { createForm } from "svelte-forms-lib";
  import { createEventDispatcher } from "svelte";
  const dispatch = createEventDispatcher();

  const { form, errors, state, handleChange, handleSubmit } = createForm({
    initialValues: {
      start_date: "",
      experiment_idenifer: "",
    },
    onSubmit: (values) => {
      dispatch("submitted", {
        experimentInfo: values,
      });
    },
  });
</script>

<form class="w-full" on:submit={handleSubmit}>
  <!-- TODO: Maybe use grid instead -->
  <div class="w-full">
    <label
      class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
      for="date_recorded">Date Recorded</label
    >
    <input
      type="date"
      id="date_recorded"
      name="date_recorded"
      class="appearance-none block w-full bg-gray-200 text-gray-700 border border-red-500 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white"
      bind:value={$form.start_date}
    />
  </div>

  <div class="w-full">
    <label
      class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
      for="experiment_id">Experiment Idenifer</label
    >
    <input
      type="text"
      id="experiment_idenifer"
      name="experiment_idenifer"
      class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
      bind:value={$form.experiment_idenifer}
    />
  </div>

  <div class="w-1/2 px-3 py-3">
    <input
      class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
      type="submit"
    />
  </div>
</form>
