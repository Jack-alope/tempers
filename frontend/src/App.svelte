<script lang="ts">
  import router from "page";

  import Navbar from "./components/Navbar.svelte";
  import Home from "./pages/Home.svelte";
  import Upload from "./pages/Upload.svelte";
  import Tracking from "./pages/Tracking.svelte";
  import Analysis from "./pages/Analysis.svelte";
  import Database from "./pages/Database.svelte";

  let page;

  router("/", () => (page = Home));
  router("/upload", () => (page = Upload));
  router("/tracking", () => (page = Tracking));
  router("/analysis", () => (page = Analysis));
  router("/database", () => (page = Database));

  router.start();
</script>

<Navbar />
<svelte:component this={page} />

<style global lang="postcss">
  @tailwind base;
  @tailwind components;
  @tailwind utilities;
</style>
