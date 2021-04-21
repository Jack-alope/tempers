<script>
  import { createEventDispatcher } from "svelte";
  export let image_path;
  export let tissue_count;

  const dispatch = createEventDispatcher();
  let calibration_distance;
  let boxes = [];
  let cal_points = [];
  let cross_points = [];

  let done = false;

  // TODO: re write all this in TS also its just gross
  function getPostCount() {
    // TODO: fix naming here
    // var id_vid = document.getElementById("videoId").value;
    initDraw(
      document.getElementById("canvas"),
      tissue_count,
      calibration_distance
    );
  }

  function initDraw(canvas, tissue_count, calibration_distance) {
    let cal_done = false;
    let crosssections = false;

    let post_count = tissue_count * 2;

    function setMousePosition(e) {
      var ev = e || window.event; //Moz || IE
      if (ev.pageX) {
        //Moz
        mouse.x = ev.pageX + window.pageXOffset;
        mouse.y = ev.pageY + window.pageYOffset;
      } else if (ev.clientX) {
        //IE
        mouse.x = ev.clientX + document.body.scrollLeft;
        mouse.y = ev.clientY + document.body.scrollTop;
      }
    }

    var mouse = {
      x: 0,
      y: 0,
      startX: 0,
      startY: 0,
    };
    var element = null;

    canvas.onmousemove = function (e) {
      setMousePosition(e);
      if (element !== null) {
        element.style.width = Math.abs(mouse.x - mouse.startX) + "px";
        element.style.height = Math.abs(mouse.y - mouse.startY) + "px";
        element.style.left =
          mouse.x - mouse.startX < 0 ? mouse.x + "px" : mouse.startX + "px";
        element.style.top =
          mouse.y - mouse.startY < 0 ? mouse.y + "px" : mouse.startY + "px";
      }
    };

    canvas.onclick = function (e) {
      if (cal_done == false) {
        if (element !== null) {
          element = null;
          canvas.style.cursor = "default";
          cal_done = true;
          console.log("finsihed.");
          cal_points.push(GetCoordinates());
          console.log(GetCoordinates());
        } else {
          console.log("begun.");
          mouse.startX = mouse.x;
          mouse.startY = mouse.y;
          element = document.createElement("div");
          element.className = "line";
          element.style.left = mouse.x + "px";
          element.style.top = mouse.y + "px";
          canvas.appendChild(element);
          canvas.style.cursor = "crosshair";
          cal_points.push(GetCoordinates());
          console.log(GetCoordinates());
        }
      } else if (crosssections == false) {
        if (element !== null) {
          element = null;
          canvas.style.cursor = "default";
          tissue_count--;
          console.log("finsihed.");
          cross_points.push(GetCoordinates());
          console.log(GetCoordinates());
          if (tissue_count == 0) {
            crosssections = true;
          }
        } else {
          console.log("begun.");
          mouse.startX = mouse.x;
          mouse.startY = mouse.y;
          element = document.createElement("div");
          element.className = "cross";
          element.style.left = mouse.x + "px";
          element.style.top = mouse.y + "px";
          canvas.appendChild(element);
          canvas.style.cursor = "crosshair";
          cross_points.push(GetCoordinates());
          console.log(GetCoordinates());
        }
      } else {
        console.log("boxes");
        if (element !== null) {
          element = null;
          canvas.style.cursor = "default";
          post_count--;
          console.log("finsihed." + post_count);
          boxes.push(GetCoordinates());
          console.log(GetCoordinates());
          if (post_count == 0) {
            done = true;
            dispatch("posts_selected", {
              boxes: boxes,
              cal_points: cal_points,
              cross_points: cross_points,
              calibration_distance: calibration_distance,
            });
          }
        } else {
          console.log("begun.");
          mouse.startX = mouse.x;
          mouse.startY = mouse.y;
          element = document.createElement("div");
          element.className = "rectangle";
          element.style.left = mouse.x + "px";
          element.style.top = mouse.y + "px";
          canvas.appendChild(element);
          canvas.style.cursor = "crosshair";
          boxes.push(GetCoordinates());
          console.log(GetCoordinates());
        }
      }
    };
  }

  function FindPosition(oElement) {
    if (typeof oElement.offsetParent != "undefined") {
      for (var posX = 0, posY = 0; oElement; oElement = oElement.offsetParent) {
        posX += oElement.offsetLeft;
        posY += oElement.offsetTop;
      }
      return [posX, posY];
    } else {
      return [oElement.x, oElement.y];
    }
  }

  function GetCoordinates(e) {
    var PosX = 0,
      PosY = 0,
      ImgPos;
    ImgPos = FindPosition(canvas);
    if (!e) var e = window.event;
    if (e.pageX || e.pageY) {
      PosX = e.pageX;
      PosY = e.pageY;
    } else if (e.clientX || e.clientY) {
      PosX =
        e.clientX +
        document.body.scrollLeft +
        document.documentElement.scrollLeft;
      PosY =
        e.clientY +
        document.body.scrollTop +
        document.documentElement.scrollTop;
    }
    PosX = PosX - ImgPos[0];
    PosY = PosY - ImgPos[1];
    return [PosX, PosY];
  }
</script>

<h1>Multi Tissue Tracking</h1>
<h5>Please select posts for {tissue_count} tissues</h5>
<!-- TODO: use session instead of hidden forms -->
<form id="number_of_posts">
  <!-- <input type="hidden" id="videoId" name="videoId" value={video_id} /> -->
  <label for="calDist">Enter the calibration Disttance (mm)</label>
  <!-- TODO: Make this look better -->
  <input
    type="number"
    step="any"
    id="calDist"
    name="calDist"
    class="appearance-none block w-1/4 bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
    bind:value={calibration_distance}
  />
  <input type="button" value="submit" on:click={() => getPostCount()} />
</form>

<div id="canvas">
  <img id="pic" src="{process.env.API_URL}/{image_path}" alt="Heart Tissue" />
</div>

<div id="container" />

<style>
</style>
