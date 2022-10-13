console.log("vegalite_vis.js loaded");

var vl_map = "../vega-lite/map_na.vl.json"
vegaEmbed("#map", vl_map)

// var vg_1 = "../vega-lite/map.vl.json"; vegaEmbed("#map", vg_1).then(function(result) {
//     // Access the Vega view instance (https://vega.github.io/vega/docs/api/view/) as result.view
//     }).catch(console.error);