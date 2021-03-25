<script lang="ts">
  import SelectPosts from "../componets/SelectPosts.svelte";
  import SelectVideo from "../componets/SelectVideo.svelte";

  import { video_id } from "../componets/Stores.js";

  let vidSelected = false;
  let num_tissues: number;
  let image_path: string;
  let video_id_value: number;

  const unsubscribe = video_id.subscribe((value) => {
    video_id_value = value;
  });

  async function handleVideoSelected() {
    vidSelected = true;
    const res = await fetch(
      process.env.url + `/selectedVideo?video_id=${video_id_value}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      }
    );

    if (res.ok) {
      const response_json = await res.json();
      image_path = response_json.image_path;
      num_tissues = response_json.number_tissues;
    } else {
      alert("Something went wrong");
    }
  }

  async function handlePostsSelected(event) {
    const boxes = event.detail.boxes;
    const cal_points = event.detail.cal_points;
    const cross_points = event.detail.cross_points;
    const calibration_distance = event.detail.calibration_distance;
    const boxes_and_id = {
      boxes,
      cal_points,
      cross_points,
      video_id_value,
      calibration_distance,
    };

    const res = await fetch(process.env.url + "/boxCoordinates", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(boxes_and_id),
    });

    if (res.ok) {
      window.location.replace("/analysis");
    } else {
      alert("Something went wrong");
    }
  }
</script>

{#if !vidSelected}
  <SelectVideo on:video_selected={handleVideoSelected} />
{:else}
  <SelectPosts
    on:posts_selected={handlePostsSelected}
    {image_path}
    {num_tissues}
    {video_id}
  />
{/if}
