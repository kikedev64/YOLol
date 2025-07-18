/*
Script to export Photoshop layer information as JSON.
This script collects all visible layers in the active document,
ignoring those that start with "_ignore", and outputs their names, positions, and dimensions in JSON format.
*/

var doc = app.activeDocument;
var json = "[\n";

var filteredLayers = [];

for (var i = 0; i < doc.layers.length; i++) {
  var layer = doc.layers[i];
  if (layer.name.indexOf("_ignore") === 0) continue;
  filteredLayers.push(layer);
}


for (var i = 0; i < filteredLayers.length; i++) {
  var layer = filteredLayers[i];

  if (!layer.isBackgroundLayer && layer.visible) {

    var bounds = layer.bounds; // [left, top, right, bottom]

    var x = Math.round(bounds[0].as("px"));
    var y = Math.round(bounds[1].as("px"));
    var width = Math.round(bounds[2].as("px") - x);
    var height = Math.round(bounds[3].as("px") - y);

    json += "  {\n";
    json += '    "name": "' + layer.name + '",\n';
    json += '    "x": ' + x + ",\n";
    json += '    "y": ' + y + ",\n";
    json += '    "width": ' + width + ",\n";
    json += '    "height": ' + height + "\n";
    json += "  }";

    if (i < filteredLayers.length - 1) {
      json += ",\n";
    } else {
      json += "\n";
    }
  }
}

json += "]";

var file = File.saveDialog("Guardar info de capas como .json", "*.json");
if (file) {
  file.encoding = "UTF8";
  file.open("w");
  file.write(json);
  file.close();
  alert("Información exportada como JSON:\n" + file.fsName);
}
