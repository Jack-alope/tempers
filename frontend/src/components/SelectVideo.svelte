<script lang="ts">
  import { onMount, createEventDispatcher } from "svelte";
  import { createForm } from "svelte-forms-lib";

  import { video_id } from "../components/Stores.js";

  const dispatch = createEventDispatcher();

  let videos = [];
  let videoGroup = -1;

  onMount(async () => {
    const res = await fetch(process.env.API_URL + "/videos");
    videos = await res.json();
  });

  // TODO: add form validations
  const { form, errors, state, handleChange, handleSubmit } = createForm({
    initialValues: {},
    onSubmit: () => {
      video_id.set(videoGroup);
      dispatch("video_selected", {});
    },
  });
</script>

<form class="w-full" on:submit={handleSubmit}>
  {#each videos as video}
    <div>
      <input
        type="radio"
        name="video"
        bind:group={videoGroup}
        value={video.id}
      />
      <!-- TODO: Make this selct form better show exp idenifiyer and bio num not ids -->
      <label for={video.id}
        >ID: {video.id}, Date Recored: {video.date_recorded}, Frequency: {video.frequency},
        Experiment_id: {video.experiment_id}, Bio Reactor_id: {video.bio_reactor_id}</label
      >
    </div>
  {/each}

  <div class="w-1/2 px-3 py-3">
    <input
      class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
      type="submit"
    />
  </div>
</form>
