<script type="ts">
  let files
  export let uploadBioReactorArchive: boolean = false


  async function addBioReactorArchive(){
    const formData = new FormData();
    formData.append("file", files[0])

    const rest = await fetch(
      process.env.API_URL + "/upload/bio_reactor_archive",
      {
        method: "POST",
        body: formData,
      }
    );

    if (rest.ok) {
        uploadBioReactorArchive = false
    } else {
        alert("Something went wrong");
    }
  }
</script>

<form class="w-full" on:submit|preventDefault={addBioReactorArchive}>
    <!-- TODO: Maybe use grid instead -->
    <div class="w-full">
  
      <div class="w-full px-3">
        <label
          class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
          for="archive">Upload Archive</label
        >
        <input
          class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
          id="archive"
          name="archive"
          type="file"
          bind:files
        />
      </div>
      <br />
  
      <div class="w-full px-3">
        <input
          class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
          type="submit"
        />
      </div>
      <br />
    </div>
  </form>


