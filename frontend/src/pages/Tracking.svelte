<script lang="ts">
  import { onMount } from "svelte";
  import SelectPosts from "../components/SelectPosts.svelte";

  let video_id: number;
  let tissue_count: number;
  let image_path: string;

  async function handleVideoSelected(video_id) {
    if (video_id) {
      const res = await fetch(
        process.env.API_URL + `/selectedVideo?video_id=${video_id}`,
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
        tissue_count = response_json.number_tissues;
      } else {
        alert("Something went wrong");
      }
    }
  }

  onMount(async () => {
    const urlParams = new URLSearchParams(window.location.search);
    video_id = parseInt(urlParams.get("video_id"));
    await handleVideoSelected(video_id);
  });

  async function handlePostsSelected(event) {
    console.log(event.detail.cal_factor);
    console.log(event.detail.cal_set_ident);
    const boxes = event.detail.boxes;
    const cal_points = event.detail.cal_points;
    const cross_points = event.detail.cross_points;
    const calibration_distance = event.detail.calibration_distance;
    const calibration_factor = event.detail.cal_factor;
    const calibration_set_identifier = event.detail.cal_set_ident;
    const boxes_and_id = {
      boxes,
      cal_points,
      cross_points,
      video_id,
      calibration_distance,
      calibration_factor,
      calibration_set_identifier,
    };

    const res = await fetch(process.env.API_URL + "/boxCoordinates", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(boxes_and_id),
    });

    if (res.ok) {
      window.location.replace(`/database`);
    } else {
      alert("Something went wrong");
    }
  }
</script>

<SelectPosts
  on:posts_selected={handlePostsSelected}
  {image_path}
  {tissue_count}
/>
