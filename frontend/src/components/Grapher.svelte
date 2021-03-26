<script>
  import { json_data_list } from "../components/Stores.js";

  import { onMount } from "svelte";

  export let nums, freqs, types, files_value;

  let json_data_list_value;

  json_data_list.subscribe((value) => {
    json_data_list_value = value;
  });

  onMount(async () => {
    grapherFunc();
  });

  async function caculate() {
    const res = await fetch(process.env.url + "/call_calcs", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(files_value),
    });
  }

  function grapherFunc() {
    let df = json_data_list_value; // document.getElementById("dataframe").value;
    df = JSON.parse(df);

    /* -----------------Define Lists for Slider Variables-----------------------*/
    var xranges = [];
    var thresholds = [];
    var polynomials = [];
    var windows = [];
    var buffers = [];
    var minDistances = [];
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
            label: "1",
            method: "restyle",
            args: ["thresh", "1"],
          },
        ],
      };
      var buffSlider = {
        len: 0.5,
        pad: {
          t: 160,
        },
        currentvalue: {
          xanchor: "right",
          prefix: "Buff: ",
          font: {
            color: "#888",
            size: 10,
          },
        },
        steps: [
          {
            label: "0",
            method: "restyle",
            args: ["buff", "0"],
          },
          {
            label: "1",
            method: "restyle",
            args: ["buff", "1"],
          },
          {
            label: "2",
            method: "restyle",
            args: ["buff", "2"],
          },
          {
            label: "3",
            method: "restyle",
            args: ["buff", "3"],
          },
          {
            label: "4",
            method: "restyle",
            args: ["buff", "4"],
          },
          {
            label: "5",
            method: "restyle",
            args: ["buff", "5"],
          },
          {
            label: "6",
            method: "restyle",
            args: ["buff", "6"],
          },
          {
            label: "7",
            method: "restyle",
            args: ["buff", "7"],
          },
          {
            label: "8",
            method: "restyle",
            args: ["buff", "8"],
          },
          {
            label: "9",
            method: "restyle",
            args: ["buff", "9"],
          },
          {
            label: "10",
            method: "restyle",
            args: ["buff", "10"],
          },
        ],
      };
      var minDistSlider = {
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
            label: "1",
            method: "restyle",
            args: ["mdist", "1"],
          },
          {
            label: "2",
            method: "restyle",
            args: ["mdist", "2"],
          },
          {
            label: "3",
            method: "restyle",
            args: ["mdist", "3"],
          },
          {
            label: "4",
            method: "restyle",
            args: ["mdist", "4"],
          },
          {
            label: "5",
            method: "restyle",
            args: ["mdist", "5"],
          },
          {
            label: "6",
            method: "restyle",
            args: ["mdist", "6"],
          },
          {
            label: "7",
            method: "restyle",
            args: ["buff", "7"],
          },
          {
            label: "8",
            method: "restyle",
            args: ["mdist", "8"],
          },
          {
            label: "9",
            method: "restyle",
            args: ["mdist", "9"],
          },
          {
            label: "10",
            method: "restyle",
            args: ["mdist", "10"],
          },
        ],
      };
      var polySlider = {
        len: 0.5,
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
          buffSlider,
          polySlider,
          windSlider,
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
      buffers.push("3");
      minDistances.push("5");
      /* ---------------------------------------------------------------------------------*/
      /* --------------------------Call Graphing Once with Defaults ---------------------------------*/
      let Div = document.getElementById(istring);
      toPython(
        xranges[Div.valueOf().id],
        thresholds[Div.valueOf().id],
        buffers[Div.valueOf().id],
        polynomials[Div.valueOf().id],
        windows[Div.valueOf().id],
        minDistances[Div.valueOf().id],
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
            buffers[Div.valueOf().id],
            polynomials[Div.valueOf().id],
            windows[Div.valueOf().id],
            minDistances[Div.valueOf().id],
            Div
          );
        } else if (typeof eventdata["xaxis.range"][0] != "undefined") {
          xranges[Div.valueOf().id][0] = eventdata["xaxis.range"][0];
          xranges[Div.valueOf().id][1] = eventdata["xaxis.range"][1];
          toPython(
            xranges[Div.valueOf().id],
            thresholds[Div.valueOf().id],
            buffers[Div.valueOf().id],
            polynomials[Div.valueOf().id],
            windows[Div.valueOf().id],
            minDistances[Div.valueOf().id],
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
            buffers[Div.valueOf().id],
            polynomials[Div.valueOf().id],
            windows[Div.valueOf().id],
            minDistances[Div.valueOf().id],
            Div
          );
        } else if (typeof eventData[0].polynom != "undefined") {
          polynomials[Div.valueOf().id] = eventData[0].polynom;
          toPython(
            xranges[Div.valueOf().id],
            thresholds[Div.valueOf().id],
            buffers[Div.valueOf().id],
            polynomials[Div.valueOf().id],
            windows[Div.valueOf().id],
            minDistances[Div.valueOf().id],
            Div
          );
        } else if (typeof eventData[0].wind != "undefined") {
          windows[Div.valueOf().id] = eventData[0].wind;
          toPython(
            xranges[Div.valueOf().id],
            thresholds[Div.valueOf().id],
            buffers[Div.valueOf().id],
            polynomials[Div.valueOf().id],
            windows[Div.valueOf().id],
            minDistances[Div.valueOf().id],
            Div
          );
        } else if (typeof eventData[0].buff != "undefined") {
          buffers[Div.valueOf().id] = eventData[0].buff;
          toPython(
            xranges[Div.valueOf().id],
            thresholds[Div.valueOf().id],
            buffers[Div.valueOf().id],
            polynomials[Div.valueOf().id],
            windows[Div.valueOf().id],
            minDistances[Div.valueOf().id],
            Div
          );
        } else if (typeof eventData[0].mdist != "undefined") {
          minDistances[Div.valueOf().id] = eventData[0].mdist;
          console.log(Div.valueOf().id);
          toPython(
            xranges[Div.valueOf().id],
            thresholds[Div.valueOf().id],
            buffers[Div.valueOf().id],
            polynomials[Div.valueOf().id],
            windows[Div.valueOf().id],
            minDistances[Div.valueOf().id],
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
    buffers,
    polynomials,
    windows,
    minDistances,
    Div
  ) {
    console.log("TO Python");
    console.log(Div);
    console.log(Div.valueOf().id);
    let value = Div.valueOf().id;
    const graph_params = {
      xrange,
      value,
      thresholds,
      buffers,
      polynomials,
      windows,
      minDistances,
      files_value,
    };
    let graph_paramsJson = JSON.stringify(graph_params);
    console.log(graph_paramsJson);

    const res = await fetch(process.env.url + "/graphUpdate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: graph_paramsJson,
    });

    if (res.ok) {
      const response = await res.json();
      Plotly.deleteTraces(Div.valueOf().id, [
        -9,
        -8,
        -7,
        -6,
        -5,
        -4,
        -3,
        -2,
        -1,
      ]);
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
      });
      Plotly.addTraces(Div.valueOf().id, {
        x: response.data.basex,
        y: response.data.basey,
        mode: "markers",
        name: "Base",
      });
      /*Plotly.addTraces(Div.valueOf().id, {x: response.data.frontx,
                                            y: response.data.fronty,
                                            mode: 'markers', name: 'Front'})
  
         */
      Plotly.addTraces(Div.valueOf().id, {
        x: response.data.tencontx,
        y: response.data.tenconty,
        mode: "markers",
        name: "Ten % Contracted",
      });
      Plotly.addTraces(Div.valueOf().id, {
        x: response.data.fifcontx,
        y: response.data.fifconty,
        mode: "markers",
        name: "Fifty % Contracted",
      });
      Plotly.addTraces(Div.valueOf().id, {
        x: response.data.ninecontx,
        y: response.data.nineconty,
        mode: "markers",
        name: "Ninety % Contracted",
      });
      Plotly.addTraces(Div.valueOf().id, {
        x: response.data.tenrelx,
        y: response.data.tenrely,
        mode: "markers",
        name: "Ten % Relaxed",
      });
      Plotly.addTraces(Div.valueOf().id, {
        x: response.data.fifrelx,
        y: response.data.fifrely,
        mode: "markers",
        name: "Fifty % Relaxed",
      });
      Plotly.addTraces(Div.valueOf().id, {
        x: response.data.ninerelx,
        y: response.data.ninerely,
        mode: "markers",
        name: "Ninety % Relaxed",
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
  on:click={caculate}>Calculate</button
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
