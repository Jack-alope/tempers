<script lang="ts">
  import { checkExpExist } from '../apiCalls'

  let files
  let experiment_idenifer: string

  export let uploadArchive = false

  async function checkExp() {
    if (await checkExpExist(experiment_idenifer)) {
      alert('Experirment Exsists uploading will over write exsisting data')
    }
  }

  async function addArchive() {
    const formData = new FormData()
    formData.append('file', files[0])

    const res = await fetch(process.env.API_URL + '/upload/experiment_archive', {
      method: 'POST',
      body: formData
    })

    if (res.ok) {
      uploadArchive = false
    } else {
      alert('Something went wrong')
    }
  }
</script>

<form class="w-full" on:submit|preventDefault={addArchive}>
  <!-- TODO: Maybe use grid instead -->
  <div class="w-full">
    <div class="w-full px-3">
      <label
        class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2"
        for="experiment_id">Experiment Idenifer</label
      >
      <input
        type="text"
        id="experiment_idenifer"
        name="experiment_idenifer"
        class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
        bind:value={experiment_idenifer}
        on:blur={checkExp}
      />
    </div>

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
