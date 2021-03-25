<script lang="ts">
  import router from "page";

  import Navbar from "./componets/Navbar.svelte";
  import Home from "./pages/Home.svelte";
  import Upload from "./pages/Upload.svelte";
  import Tracking from "./pages/Tracking.svelte";
  import Analysis from "./pages/Analysis.svelte";

  let page;

  router("/", () => (page = Home));
  router("/upload", () => (page = Upload));
  router("/tracking", () => (page = Tracking));
  router("/analysis", () => (page = Analysis));

  router.start();
</script>

<Navbar />
<svelte:component this={page} />

<style global lang="postcss">
  @tailwind base;
  @tailwind components;
  @tailwind utilities;
</style>
