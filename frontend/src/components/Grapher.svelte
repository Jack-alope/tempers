<script>
  import { onMount } from "svelte";
  import { saveAs } from "file-saver";

  import { json_data_list } from "../components/Stores.js";

  export let nums,
    freqs,
    types,
    video_id = null,
    experiment_identifier = null,
    tissue_number = null;

  let json_data_list_value;

  json_data_list.subscribe((value) => {
    json_data_list_value = value;
  });

  onMount(async () => {
    grapherFunc();
  });

  async function caculate() {
    let url;
    if (video_id) {
      url = `/caculate?video_id=${video_id}`;
    } else {
      url = `/caculate?experiment_identifier=${experiment_identifier}&tissue_number=${tissue_number}`;
    }
    const res = await fetch(process.env.API_URL + url, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });
    if (res.ok) {
      const file = await res.blob();
      if (file) {
        const blob = new Blob([file]);
        if (video_id) {
          saveAs(blob, `${video_id}_calculations.csv`);
        } else {
          saveAs(
            blob,
            `${experiment_identifier}_${tissue_number}_calculations.csv`
          );
        }
      }
    }
  }

  function grapherFunc() {
    let df = json_data_list_value; // document.getElementById("dataframe").value;
    df = JSON.parse(df);

    /* -----------------Define Lists for Slider Variables-----------------------*/
    var xranges = [];
    var thresholds = [];
    var polynomials = [];
    var windows = [];
    var minDistances = [];
    var buffers = [];
    /* -----------------------------------------------------------------------------------*/

    for (var i = 0; i < df.length; i++) {
      var istring = i.toString();
      df[i] = JSON.parse(df[i]);

      /* --------------Define Data Start-----------------------------------------------*/
      var disp_graph = {
        x: Object.values(df[i].time),
        y: Object.values(df[i].disp),
        mode: "scatter",
        name: "Disp",
      };
      var temp = {
        x: [],
        y: [],
        mode: "markers",
      };
      var data = [
        disp_graph,
        temp,
        temp,
        temp,
        temp,
        temp,
        temp,
        temp,
        temp,
        temp,
      ];
      /* ------------------------------------------------------------------------------------*/

      /* ---------------Define Sliders Start------------------------------------------------*/
      var threshSlider = {
        active: 6,
        len: 0.5,
        pad: {
          t: 100,
        },
        currentvalue: {
          xanchor: "right",
          prefix: "Thresh: ",
          font: {
            color: "#888",
            size: 10,
          },
        },
        steps: [
          {
            label: "0",
            method: "restyle",
            args: ["thresh", "0"],
          },
          {
            label: ".1",
            method: "restyle",
            args: ["thresh", ".1"],
          },
          {
            label: ".2",
            method: "restyle",
            args: ["thresh", ".2"],
          },
          {
            label: ".3",
            method: "restyle",
            args: ["thresh", ".3"],
          },
          {
            label: ".4",
            method: "restyle",
            args: ["thresh", ".4"],
          },
          {
            label: ".5",
            method: "restyle",
            args: ["thresh", ".5"],
          },
          {
            label: ".6",
            method: "restyle",
            args: ["thresh", ".6"],
          },
          {
            label: ".7",
            method: "restyle",
            args: ["thresh", ".7"],
          },
          {
            label: ".8",
            method: "restyle",
            args: ["thresh", ".8"],
          },
          {
            label: ".9",
            method: "restyle",
            args: ["thresh", ".9"],
          },
          {
            label: ".99",
            method: "restyle",
            args: ["thresh", ".99"],
          },
        ],
      };
      var minDistSlider = {
        active: 0,
        len: 0.5,
        x: 0.5,
        pad: {
          t: 100,
        },
        currentvalue: {
          xanchor: "right",
          prefix: "minDist: ",
          font: {
            color: "#888",
            size: 10,
          },
        },
        steps: [
          {
            label: "0",
            method: "restyle",
            args: ["mdist", "0"],
          },
          {
            label: "5",
            method: "restyle",
            args: ["mdist", "5"],
          },
          {
            label: "10",
            method: "restyle",
            args: ["mdist", "10"],
          },
          {
            label: "15",
            method: "restyle",
            args: ["mdist", "15"],
          },
          {
            label: "20",
            method: "restyle",
            args: ["mdist", "20"],
          },
          {
            label: "25",
            method: "restyle",
            args: ["mdist", "25"],
          },
          {
            label: "30",
            method: "restyle",
            args: ["mdist", "30"],
          },
          {
            label: "35",
            method: "restyle",
            args: ["mdist", "35"],
          },
          {
            label: "40",
            method: "restyle",
            args: ["mdist", "40"],
          },
          {
            label: "45",
            method: "restyle",
            args: ["mdist", "45"],
          },
          {
            label: "50",
            method: "restyle",
            args: ["mdist", "50"],
          },
          {
            label: "55",
            method: "restyle",
            args: ["mdist", "55"],
          },
          {
            label: "60",
            method: "restyle",
            args: ["mdist", "60"],
          },
          {
            label: "65",
            method: "restyle",
            args: ["mdist", "65"],
          },
          {
            label: "70",
            method: "restyle",
            args: ["mdist", "70"],
          },
          {
            label: "75",
            method: "restyle",
            args: ["mdist", "75"],
          },
          {
            label: "80",
            method: "restyle",
            args: ["mdist", "80"],
          },
          {
            label: "85",
            method: "restyle",
            args: ["mdist", "85"],
          },
          {
            label: "90",
            method: "restyle",
            args: ["mdist", "90"],
          },
          {
            label: "95",
            method: "restyle",
            args: ["mdist", "9555"],
          },
          {
            label: "100",
            method: "restyle",
            args: ["mdist", "100"],
          },
        ],
      };
      var bufferSlider = {
        active: 0,
        len: 0.5,
        pad: {
          t: 160,
        },
        currentvalue: {
          xanchor: "left",
          prefix: "Buffer: ",
          font: {
            color: "#888",
            size: 10,
          },
        },
        steps: [
          {
            label: "0",
            method: "restyle",
            args: ["buffer", "0"],
          },
          {
            label: "5",
            method: "restyle",
            args: ["buffer", "5"],
          },
          {
            label: "10",
            method: "restyle",
            args: ["buffer", "10"],
          },
          {
            label: "15",
            method: "restyle",
            args: ["buffer", "15"],
          },
          {
            label: "20",
            method: "restyle",
            args: ["buffer", "20"],
          },
          {
            label: "25",
            method: "restyle",
            args: ["buffer", "25"],
          },
          {
            label: "30",
            method: "restyle",
            args: ["buffer", "30"],
          },
          {
            label: "35",
            method: "restyle",
            args: ["buffer", "35"],
          },
          {
            label: "40",
            method: "restyle",
            args: ["buffer", "40"],
          },
          {
            label: "45",
            method: "restyle",
            args: ["buffer", "45"],
          },
          {
            label: "50",
            method: "restyle",
            args: ["buffer", "50    print(data.buffers)"],
          },
        ],
      };
      var polySlider = {
        len: 0.5,
        active: 0,
        pad: {
          t: 220,
        },
        currentvalue: {
          xanchor: "right",
          prefix: "Poly: ",
          font: {
            color: "#888",
            size: 10,
          },
        },
        steps: [
          {
            label: "3",
            method: "restyle",
            args: ["polynom", "3"],
          },
          {
            label: "4",
            method: "restyle",
            args: ["polynom", "4"],
          },
          {
            label: "5",
            method: "restyle",
            args: ["polynom", "5"],
          },
          {
            label: "6",
            method: "restyle",
            args: ["polynom", "6"],
          },
          {
            label: "7",
            method: "restyle",
            args: ["polynom", "7"],
          },
          {
            label: "8",
            method: "restyle",
            args: ["polynom", "8"],
          },
          {
            label: "9",
            method: "restyle",
            args: ["polynom", "9"],
          },
          {
            label: "10",
            method: "restyle",
            args: ["polynom", "10"],
          },
        ],
      };
      var windSlider = {
        active: 1,
        len: 0.5,
        x: 0.5,
        currentvalue: {
          xanchor: "right",
          prefix: "Wind: ",
          font: {
            color: "#888",
            size: 10,
          },
        },
        pad: {
          t: 210,
        },
        steps: [
          {
            label: "11",
            method: "restyle",
            args: ["wind", "11"],
          },
          {
            label: "13",
            method: "restyle",
            args: ["wind", "13"],
          },
          {
            label: "15",
            method: "restyle",
            args: ["wind", "15"],
          },
          {
            label: "17",
            method: "restyle",
            args: ["wind", "17"],
          },
          {
            label: "19",
            method: "restyle",
            args: ["wind", "19"],
          },
          {
            label: "21",
            method: "restyle",
            args: ["wind", "21"],
          },
          {
            label: "23",
            method: "restyle",
            args: ["wind", "23"],
          },
          {
            label: "25",
            method: "restyle",
            args: ["wind", "25"],
          },
        ],
      };
      /* -----------------------------------------------------------------------------------*/

      /* ---------------Set Layout and Graph----------------------------------------------*/
      var layout = {
        xaxis: {
          rangeslider: {},
        },
        sliders: [
          threshSlider,
          minDistSlider,
          polySlider,
          windSlider,
          bufferSlider,
        ],
      };

      Plotly.newPlot(istring, data, layout);
      /* ------------------------------------------------------------------------------------*/

      /* -----------------Set Default Slider Values-----------------------------------------*/
      var temp = [0, 0];
      xranges.push(temp);
      thresholds.push(".6");
      polynomials.push("3");
      windows.push("13");
      minDistances.push("0");
      buffers.push("0");
      /* ---------------------------------------------------------------------------------*/
      /* --------------------------Call Graphing Once with Defaults ---------------------------------*/
      let Div = document.getElementById(istring);
      toPython(
        xranges[Div.valueOf().id],
        thresholds[Div.valueOf().id],
        polynomials[Div.valueOf().id],
        windows[Div.valueOf().id],
        minDistances[Div.valueOf().id],
        buffers[Div.valueOf().id],
        Div
      );
      /* ---------------------------------------------------------------------------------------------------*/
      /* ----------------Range Selector----------------------------------------------*/
      Div.on("plotly_relayout", function (eventdata) {
        // TODO: This is clearly a plotly typo, maybe notify them/open pull request
        if (typeof eventdata["xaxis.range[0]"] != "undefined") {
          xranges[Div.valueOf().id][0] = eventdata["xaxis.range[0]"];
          xranges[Div.valueOf().id][1] = eventdata["xaxis.range[1]"];
          toPython(
            xranges[Div.valueOf().id],
            thresholds[Div.valueOf().id],
            polynomials[Div.valueOf().id],
            windows[Div.valueOf().id],
            minDistances[Div.valueOf().id],
            buffers[Div.valueOf().id],
            Div
          );
        } else if (typeof eventdata["xaxis.range"][0] != "undefined") {
          xranges[Div.valueOf().id][0] = eventdata["xaxis.range"][0];
          xranges[Div.valueOf().id][1] = eventdata["xaxis.range"][1];
          toPython(
            xranges[Div.valueOf().id],
            thresholds[Div.valueOf().id],
            polynomials[Div.valueOf().id],
            windows[Div.valueOf().id],
            minDistances[Div.valueOf().id],
            buffers[Div.valueOf().id],
            Div
          );
        }
      });
      /* ---------------------------------------------------------------------------------*/

      /* ----------------Sliders Update---------------------------------------*/
      Div.on("plotly_restyle", function (eventData) {
        //Finds which slider was changed, updates that value, and calls toPython function
        if (typeof eventData[0].thresh != "undefined") {
          thresholds[Div.valueOf().id] = eventData[0].thresh;
          toPython(
            xranges[Div.valueOf().id],
            thresholds[Div.valueOf().id],
            polynomials[Div.valueOf().id],
            windows[Div.valueOf().id],
            minDistances[Div.valueOf().id],
            buffers[Div.valueOf().id],
            Div
          );
        } else if (typeof eventData[0].polynom != "undefined") {
          polynomials[Div.valueOf().id] = eventData[0].polynom;
          toPython(
            xranges[Div.valueOf().id],
            thresholds[Div.valueOf().id],
            polynomials[Div.valueOf().id],
            windows[Div.valueOf().id],
            minDistances[Div.valueOf().id],
            buffers[Div.valueOf().id],
            Div
          );
        } else if (typeof eventData[0].wind != "undefined") {
          windows[Div.valueOf().id] = eventData[0].wind;
          toPython(
            xranges[Div.valueOf().id],
            thresholds[Div.valueOf().id],
            polynomials[Div.valueOf().id],
            windows[Div.valueOf().id],
            minDistances[Div.valueOf().id],
            buffers[Div.valueOf().id],
            Div
          );
        } else if (typeof eventData[0].mdist != "undefined") {
          minDistances[Div.valueOf().id] = eventData[0].mdist;
          console.log(Div.valueOf().id);
          toPython(
            xranges[Div.valueOf().id],
            thresholds[Div.valueOf().id],
            polynomials[Div.valueOf().id],
            windows[Div.valueOf().id],
            minDistances[Div.valueOf().id],
            buffers[Div.valueOf().id],
            Div
          );
        } else if (typeof eventData[0].buffer != "undefined") {
          buffers[Div.valueOf().id] = eventData[0].buffer;
          console.log(Div.valueOf().id);
          toPython(
            xranges[Div.valueOf().id],
            thresholds[Div.valueOf().id],
            polynomials[Div.valueOf().id],
            windows[Div.valueOf().id],
            minDistances[Div.valueOf().id],
            buffers[Div.valueOf().id],
            Div
          );
        }
      });
      /* -----------------------------------------------------------------------------------*/
    }
  }

  async function toPython(
    xrange,
    thresholds,
    polynomials,
    windows,
    minDistances,
    buffers,
    Div
  ) {
    let value = Div.valueOf().id;
    let graph_params;

    if (video_id) {
      graph_params = {
        xrange,
        value,
        thresholds,
        polynomials,
        windows,
        minDistances,
        buffers,
        video_id,
      };
    } else {
      graph_params = {
        xrange,
        value,
        thresholds,
        polynomials,
        windows,
        minDistances,
        buffers,
        experiment_identifier,
        tissue_number,
      };
    }

    let graph_paramsJson = JSON.stringify(graph_params);
    console.log(graph_paramsJson);

    const res = await fetch(process.env.API_URL + "/graphUpdate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: graph_paramsJson,
    });

    if (res.ok) {
      const response = await res.json();
      Plotly.deleteTraces(Div.valueOf().id, [-6, -5, -4, -3, -2, -1]);
      Plotly.restyle(
        Div.valueOf().id,
        "y",
        [response.data.ys],
        "x",
        [response.data.xs],
        [0]
      );
      Plotly.addTraces(Div.valueOf().id, {
        x: response.data.peaksx,
        y: response.data.peaksy,
        mode: "markers",
        name: "Peaks",
        marker: {
          color: "rgb(255, 179, 0)",
          symbol: "triangle-up-dot",
          size: 10,
          line: {
            width: 1.5,
          },
        },
      });
      Plotly.addTraces(Div.valueOf().id, {
        x: response.data.basex,
        y: response.data.basey,
        mode: "markers",
        name: "Base",
        marker: {
          color: "rgba(17, 157, 255,0.5)",
          symbol: "triangle-right-dot",
          size: 10,
          line: {
            width: 1.5,
          },
        },
      });
      Plotly.addTraces(Div.valueOf().id, {
        x: response.data.frontx,
        y: response.data.fronty,
        mode: "markers",
        name: "Front",
        marker: {
          symbol: "triangle-left-dot",
          size: 10,
          line: {
            width: 1.5,
          },
        },
        visible: "legendonly",
      });
      Plotly.addTraces(Div.valueOf().id, {
        x: response.data.contractx,
        y: response.data.contracty,
        mode: "markers",
        name: "Contractpoints (10, 50, 90%)",
        marker: {
          color: "rgb(0, 131, 87)",
          symbol: "circle-open-dot",
          size: 7,
          line: {
            width: 1.5,
          },
        },
      });
      Plotly.addTraces(Div.valueOf().id, {
        x: response.data.relaxx,
        y: response.data.relaxy,
        mode: "markers",
        name: "Relaxpoints (10, 50, 80, 90%)",
        marker: {
          color: "rgb(233, 0, 0)",
          symbol: "circle-open-dot",
          size: 7,
          line: {
            width: 1.5,
          },
        },
      });
      Plotly.addTraces(Div.valueOf().id, {
        x: response.data.rawx,
        y: response.data.rawy,
        mode: "scatter",
        name: "Raw",
        visible: "legendonly",
      });
    }
  }
</script>

<button
  id="Caculate"
  class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
  on:click={() => caculate()}>Download Analysis summary</button
>

{#each nums as num, i}
  <div class="row">
    <div class="col">
      <div class="card shadow mb-4">
        <div>
          <h6 class="text-primary justfy-center font-weight-bold m-0">
            Tissue: {nums[i]} Freq: {freqs[i]} Type: {types[i]}
          </h6>
        </div>
        <div class="card-body">
          <div style="height: 600px;" id={String(i)} />
        </div>
      </div>
    </div>
  </div>
{/each}
