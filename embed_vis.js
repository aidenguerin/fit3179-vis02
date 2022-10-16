console.log("vegalite_vis.js loaded");

var vl_map_na = "vega-lite/map_na.vl.json"
vegaEmbed("#map_na", vl_map_na)

var vl_map_aunz = "vega-lite/map_aunz.vl.json"
vegaEmbed("#map_aunz", vl_map_aunz)

var vl_bar_lifts = "vega-lite/total_lifts.vl.json"
vegaEmbed("#bar_lifts", vl_bar_lifts)

var vl_bar_runs = "vega-lite/terrain_difficulty.vl.json"
vegaEmbed("#bar_runs", vl_bar_runs)

// var vg_1 = "../vega-lite/map.vl.json"; vegaEmbed("#map", vg_1).then(function(result) {
//     // Access the Vega view instance (https://vega.github.io/vega/docs/api/view/) as result.view
//     }).catch(console.error);