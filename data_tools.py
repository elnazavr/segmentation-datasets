from __future__ import  division
import json
import pandas as pd
import IPython.display
from IPython.core.display import display, HTML, Javascript
from matplotlib import pyplot as plt
import numpy as np
from matplotlib_venn_wordcloud import venn2_wordcloud, venn3_wordcloud
from matplotlib_venn import venn2
import matplotlib.pyplot as plt

def get_json_from_files(filename):
    lines = get_list_from_files(filename)
    dict_children = []
    for line in lines:
        if line!="":
            mas = line.split(":")
            dict_children.append({"name": mas[0], "size": mas[1]})
    return dict_children


def get_dict_from_file(filename):
    lines = get_list_from_files(filename)
    dict_children = {}
    for line in lines:
        if line!="":
            mas = line.split(":")
            dict_children[mas[0]] = int(mas[1])
    return dict_children
 
    
def get_list_from_files(filename):
    with open(filename, "r") as f:
        txt = f.read()
    lines = txt.split("\n")
    return lines


def get_names_from_files(filename):
    with open(filename, "r") as f:
        txt = f.read()
    lines = txt.split("\n")
    names =[]
    for line in lines:
        names.append(line.split(":")[0])
    return names


def draw_word_venn(datasets, dataset_name1, dataset_name2):
    fig, ax = plt.subplots(1,1, figsize=(30,30))
    set1 = set(get_names_from_files(datasets[dataset_name1]))
    set2 = set(get_names_from_files(datasets[dataset_name2]))
    v = venn2_wordcloud([set1, set2], (dataset_name1, dataset_name2), ax= ax, set_colors = ['blue', 'yellow'])
    for text in v.set_labels:
        text.set_fontsize(30)
    for text in v.subset_labels:
        text.set_fontsize(18)
    plt.show()

    
def draw_venn(datasets, dataset_name1, dataset_name2):
    fig, ax = plt.subplots(1,1, figsize=(30,30))
    set1 = set(get_names_from_files(datasets[dataset_name1]))
    set2 = set(get_names_from_files(datasets[dataset_name2]))
    v = venn2([set1, set2], (dataset_name1, dataset_name2), ax= ax, set_colors = ['blue', 'yellow'])
    for text in v.set_labels:
        text.set_fontsize(30)
    for text in v.subset_labels:
        text.set_fontsize(18)    
    plt.show()


def draw_word_venn_3(datasets, dataset_name1, dataset_name2, dataset_name3):
    fig, ax = plt.subplots(1,1, figsize=(30,30))
    set1 = set(get_names_from_files(datasets[dataset_name1]))
    set2 = set(get_names_from_files(datasets[dataset_name2]))
    set3 = set(get_names_from_files(datasets[dataset_name3]))
    v = venn3_wordcloud([set1, set2, set3], (dataset_name1, dataset_name2, dataset_name3), ax= ax, set_colors = ['blue', 'yellow', 'green'])
    for text in v.set_labels:
        text.set_fontsize(30)
    for text in v.subset_labels:
        text.set_fontsize(18)
    plt.show()


def draw_bar_chart(objects, performance, y_label, x_label, title):
    y_pos = np.arange(len(objects))
    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel(y_label)
    plt.xlabel(x_label)
    plt.title(title)
    plt.show()

    
def draw_all_datasets(dataset_filenames):
    children = []
    for dataset in dataset_filenames:
        filename = dataset_filenames[dataset]
        children.append({"name": dataset.upper(),  "children":get_json_from_files(filename)})
    json_structure = {"name": "flare", "children": children}
    with open('output.json', 'w') as outfile:  
        json.dump(json_structure, outfile)
    pd.read_json('output.json')


    #Embedding the html string
    html_string = """
    <!DOCTYPE html>
    <meta charset="utf-8">
    <style>

    .node {
      cursor: pointer;
    }

    .node:hover {
      stroke: #000;
      stroke-width: 1.5px;
    }

    .node--leaf {
      fill: white;
    }

    .label {
      font: 11px "Helvetica Neue", Helvetica, Arial, sans-serif;
      text-anchor: middle;
      text-shadow: 0 1px 0 #fff, 1px 0 0 #fff, -1px 0 0 #fff, 0 -1px 0 #fff;
    }

    .label,
    .node--root,
    .node--leaf {
      pointer-events: none;
    }

    </style>
    <svg width="760" height="760"></svg>
    """
    # Finally embed the D3.js to produce the circular treemap
    js_string="""
     require.config({
        paths: {
            d3: "https://d3js.org/d3.v4.min"
         }
     });

      require(["d3"], function(d3) {

       console.log(d3);

    var svg = d3.select("svg"),
        margin = 40,
        diameter = +svg.attr("width"),
        g = svg.append("g").attr("transform", "translate(" + diameter / 2 + "," + diameter / 2 + ")");

    var color = d3.scaleSequential(d3.interpolateViridis)
        .domain([-4, 4]);

    var pack = d3.pack()
        .size([diameter - margin, diameter - margin])
        .padding(2);

    d3.json("output.json", function(error, root) {
      if (error) throw error;

      root = d3.hierarchy(root)
          .sum(function(d) { return d.size; })
          .sort(function(a, b) { return b.value - a.value; });

      var focus = root,
          nodes = pack(root).descendants(),
          view;

      var circle = g.selectAll("circle")
        .data(nodes)
        .enter().append("circle")
          .attr("class", function(d) { return d.parent ? d.children ? "node" : "node node--leaf" : "node node--root"; })
          .style("fill", function(d) { return d.children ? color(d.depth) : null; })
          .on("click", function(d) { if (focus !== d) zoom(d), d3.event.stopPropagation(); });

      var text = g.selectAll("text")
        .data(nodes)
        .enter().append("text")
          .attr("class", "label")
          .style("fill-opacity", function(d) { return d.parent === root ? 1 : 0; })
          .style("display", function(d) { return d.parent === root ? "inline" : "none"; })
          .text(function(d) { return d.data.name; });

      var node = g.selectAll("circle, text");

      svg
          .style("background", color(-1))
          .on("click", function() { zoom(root); });

      zoomTo([root.x, root.y, root.r * 2 + margin]);

      function zoom(d) {
        var focus0 = focus; focus = d;

        var transition = d3.transition()
            .duration(d3.event.altKey ? 7500 : 750)
            .tween("zoom", function(d) {
              var i = d3.interpolateZoom(view, [focus.x, focus.y, focus.r * 2 + margin]);
              return function(t) { zoomTo(i(t)); };
            });

        transition.selectAll("text")
          .filter(function(d) { return d.parent === focus || this.style.display === "inline"; })
            .style("fill-opacity", function(d) { return d.parent === focus ? 1 : 0; })
            .on("start", function(d) { if (d.parent === focus) this.style.display = "inline"; })
            .on("end", function(d) { if (d.parent !== focus) this.style.display = "none"; });
      }

      function zoomTo(v) {
        var k = diameter / v[2]; view = v;
        node.attr("transform", function(d) { return "translate(" + (d.x - v[0]) * k + "," + (d.y - v[1]) * k + ")"; });
        circle.attr("r", function(d) { return d.r * k; });
      }
    });
      });
     """
    h = display(HTML(html_string))
    j = IPython.display.Javascript(js_string)
    IPython.display.display_javascript(j)