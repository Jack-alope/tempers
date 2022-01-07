<script lang="ts">
  import { createForm } from "svelte-forms-lib";

  import { showBioReactor, bio_reactors } from "../components/Stores.js";

  async function handleBioReactorSubmitted(bio_reactor_info) {
    const res = await fetch(process.env.API_URL + "/addBioReactor", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(bio_reactor_info),
    });

    if (res.ok) {
      showBioReactor.set(false);
      if ($bio_reactors) {
        $bio_reactors.push(await res.json());
      }
    } else {
      if (res.status == 409) {
        alert("Bio Number is taken");
      } else {
        alert("Something went wrong");
      }
    }
  }

  const { form, errors, state, handleChange, handleSubmit } = createForm({
    initialValues: {
      date_added: "",
      bio_reactor_number: "",
      bio_reactor_note: "",
      post_distance: 6,
      youngs_modulus: 1.33,
      posts: [
        {
          post_number: "",
          left_post_height: "",
          left_tissue_height: "",
          right_post_height: "",
          right_tissue_height: "",
          radius: "",
        },
      ],
    },
    onSubmit: (values) => {
      console.log(values);
      handleBioReactorSubmitted(values);
    },
  });

  const add = () => {
    $form.posts = $form.posts.concat({
      post_number: "",
      left_post_height: "",
      left_tissue_height: "",
      right_post_height: "",
      right_tissue_height: "",
      radius: "",
    });
    // $errors.posts = $posts.posts.concat({ name: "", email: "" });
  };

  const remove = (i) => () => {
    $form.posts = $form.posts.filter((u, j) => j !== i);
    // $errors.posts = $errors.posts.filter((u, j) => j !== i);
  };
</script>

<form class="w-full" on:submit={handleSubmit}>
  <!-- TODO: Maybe use grid instead -->

  <div class="w-full px-3 py-5">
    <h1
      class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
    >
      Add posts
    </h1>

    {#each $form.posts as tissue, j}
      <div class="flex flex-wrap py-3">
        <div class="w-full md:w-1/5 px-3">
          <input
            type="number"
            name={`posts[${j}].post_number`}
            placeholder="Post Number"
            on:change={handleChange}
            on:blur={handleChange}
            class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
            bind:value={$form.posts[j].post_number}
          />
        </div>

        <div class="w-full md:w-1/5 px-3">
          <input
            type="number"
            step="any"
            placeholder="Left Post Height"
            name={`posts[${j}].left_post_height`}
            on:change={handleChange}
            on:blur={handleChange}
            class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
            bind:value={$form.posts[j].left_post_height}
          />
        </div>

        <div class="w-full md:w-1/5 px-3">
          <input
            type="number"
            step="any"
            placeholder="Left Tissue Height"
            name={`posts[${j}].left_tissue_height`}
            on:change={handleChange}
            on:blur={handleChange}
            class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
            bind:value={$form.posts[j].left_tissue_height}
          />
        </div>

        <div class="w-full md:w-1/5 px-3">
          <input
            type="number"
            step="any"
            placeholder="Right Post Height"
            name={`posts[${j}].right_post_height`}
            on:change={handleChange}
            on:blur={handleChange}
            class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
            bind:value={$form.posts[j].right_post_height}
          />
        </div>

        <div class="w-full md:w-1/5 px-3">
          <input
            type="number"
            step="any"
            placeholder="Right Tissue Height"
            name={`posts[${j}].right_tissue_height`}
            on:change={handleChange}
            on:blur={handleChange}
            class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
            bind:value={$form.posts[j].right_tissue_height}
          />
        </div>

        <div class="w-full md:w-1/5 px-3">
          <input
            type="number"
            step="any"
            placeholder="Radius"
            name={`posts[${j}].radius`}
            on:change={handleChange}
            on:blur={handleChange}
            class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
            bind:value={$form.posts[j].radius}
          />
        </div>

        <div class="w-full md:w-1/4 px-3">
          {#if $form.posts.length !== 1}
            <button
              class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
              type="button"
              on:click={remove(j)}>-</button
            >
          {/if}

          {#if j === $form.posts.length - 1}
            <button
              class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
              type="button"
              on:click={add}>+</button
            >
          {/if}
        </div>
      </div>
    {/each}

    <div class="flex flex-wrap py-3">
      <div class="w-1/2 px-3">
        <label
          class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
          for="date_recorded">Date</label
        >
        <input
          type="date"
          id="date_recorded"
          name="date_recorded"
          class="appearance-none block w-full bg-gray-200 text-gray-700 border border-red-500 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white"
          bind:value={$form.date_added}
        />
      </div>

      <div class="w-1/2 px-3">
        <label
          class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
          for="experiment_id">Bio Reactor Number</label
        >
        <input
          type="number"
          id="bio_reactor_number"
          name="bio_reactor_number"
          class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
          bind:value={$form.bio_reactor_number}
        />
      </div>
    </div>

    <div class="flex flex-wrap py-3">
      <div class="w-1/2 px-3">
        <label
          class="block tracking-wide text-gray-700 text-xs font-bold mb-2"
          for="post_distance">POST DISTANCE (mm)</label
        >
        <input
          type="number"
          step="any"
          id="post_distance"
          name="post_distance"
          class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
          bind:value={$form.post_distance}
        />
      </div>

      <div class="w-1/2 px-3">
        <label
          class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
          for="youngs_modulus">YOUNGS MODULUS (MPa)</label
        >
        <input
          type="number"
          step="any"
          id="youngs_modulus"
          name="youngs_modulus"
          class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
          bind:value={$form.youngs_modulus}
        />
      </div>
    </div>

    <div class="flex flex-wrap py-3">
      <div class="w-1/2 px-3 py-3">
        <label
          class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
          for="vid">Bio Reactor Note</label
        >
        <input
          class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
          type="text"
          id="video_note"
          name="video_note"
          bind:value={$form.bio_reactor_note}
        />
      </div>

      <div class="w-1/2 px-3 py-5">
        <input
          class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
          type="submit"
        />
      </div>
    </div>
  </div>
</form>
