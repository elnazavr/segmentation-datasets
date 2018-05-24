from __future__ import  division
import json
import pandas as pd
import IPython.display
from IPython.core.display import display, HTML, Javascript
import numpy as np
import matplotlib.pyplot as plt
from pandas.plotting import parallel_coordinates
import plotly.plotly as py
import plotly





def get_json_from_files(filename):
    lines = get_list_from_files(filename)
    dict_children = []
    for line in lines:
        if line!="":
            mas = line.split(":")
            if len(mas)>1:
                dict_children.append({"name": mas[0], "size": mas[1]})
            else:
                dict_children.append({"name": mas[0], "size": 10})
    return dict_children


def get_dict_from_file(filename):
    lines = get_list_from_files(filename)
    dict_children = {}
    for line in lines:
        if line!="":
            mas = line.split(":")
            if len(mas)>1:
                dict_children[mas[0]] = int(mas[1])
            else:
                dict_children[mas[0]] = 0
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

def draw_chart(x, y, chart_title, x_label=None, y_label=None, title=None):
    if chart_title=='bar':
        bar_chart(x, y, y_label, x_label, title)
    elif chart_title == 'radial':
        radial_chart(x, y, title=title)
    elif chart_title == 'pie':
        donut_chart(x, y, False, title=title)
    elif chart_title == 'donut':
        donut_chart(x, y, True, title=title)
    elif chart_title == 'stacked_barh':
        dict = {x_i:y_i for x_i,y_i in zip(x,y)}
        df = pd.DataFrame(dict, index=['datasets'])
        df.plot.barh(stacked=True)
    else:
        print("Supported methods bar, radial, pie, donut, stacked_barh")
    
    
def bar_chart(x, y, x_label='', y_label='', title='', figsize=(5,5)):
    y_pos = np.arange(len(x))
    plt.figure(figsize=figsize)
    plt.bar(y_pos, y, align='center', alpha=0.5)
    plt.xticks(y_pos, x)
    plt.ylabel(y_label)
    plt.xlabel(x_label)
    plt.title(title)
    plt.show()


def radial_chart(x, y, x_label='', y_label='', title='', figsize=(5,5)):
    iN = len(x)
    arrCnts = np.array(x)

    theta=np.arange(0,2*np.pi,2*np.pi/iN)
    width = (2*np.pi)/iN *0.9
    bottom = 50

    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes([0.1, 0.1, 0.75, 0.75], polar=True)
    bars = ax.bar(theta, arrCnts, width=width, bottom=bottom)

    plt.axis('off')

    rotations = np.rad2deg(theta)
    for x, bar, rotation, label in zip(theta, bars, rotations, y):
        lab = ax.text(x,bottom+bar.get_height() , label, 
                 ha='left', va='center', rotation=rotation, rotation_mode="anchor",)   
    
    plt.ylabel(y_label)
    plt.xlabel(x_label)
    plt.title(title)
    plt.show()


def donut_chart(labels, sizes, donut,  x_label='', y_label='', title='', figsize=(5,5)):
    plt.pie(sizes, labels=labels,
            autopct='%1.1f%%', shadow=True)
    fig = plt.gcf()
    if donut:
        centre_circle = plt.Circle((0,0),0.75,color='black', fc='white',linewidth=1.25)
        fig.gca().add_artist(centre_circle)
    plt.axis('equal')
    plt.ylabel(y_label)
    plt.xlabel(x_label)
    plt.title(title)
    plt.show()



def interactive_all_datasets(dataset_filenames):
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

def show_parallel_sets(labels, colors, link, title, width=1000, height=2500):
    plotly.offline.init_notebook_mode()

    data = dict(
        type='sankey',
        node = dict(
          pad = 15,
          thickness = 20,
          line = dict(
            color = "black",
            width = 0.5
          ),
          label = labels,
          color = colors
        ),
        link = link)

    layout = dict(
        autosize = True,
        width = width,
        height = height,
        title = title,
        font = dict(
          size = 10
        )
    )

    fig = dict(data=[data], layout=layout)
    return fig

def parallel_sets(all_objects_df, intresection =1):
    objects = all_objects_df[all_objects_df.astype(bool).sum(axis=1) >=intresection]
    offset = len(objects.index)
    labels = list(objects.index) + list(objects.columns)
    colors = 'blue'

    X, Y = np.mgrid[0:len(objects.index), 0:len(objects.columns)]  # W is here as homo coordinate
    edges = np.vstack([X.ravel(), Y.ravel()])

    link = dict(
        source=edges[0, :],
        target=offset + edges[1, :],
        value=objects.as_matrix()[X, Y].flatten(),
    )

    fig = show_parallel_sets(labels, colors, link, "Parallel sets for labels in %d or more datasets", (intresection))
    plotly.offline.iplot(fig, image_width=fig['layout']['width'], image_height=fig['layout']['height'])

def visualize_matrix_dist(matrix):
    from sklearn import manifold
    adist = np.array(matrix)
    amax = np.amax(adist)
    adist /= amax

    mds = manifold.MDS(n_components=2, dissimilarity="precomputed", random_state=6)
    results = mds.fit(adist)

    coords = results.embedding_

    plt.subplots_adjust(bottom=0.1)
    plt.scatter(
        coords[:, 0], coords[:, 1], marker='o'
    )
    for label, x, y in zip(matrix.columns, coords[:, 0], coords[:, 1]):
        plt.annotate(
            label,
            xy=(x, y), xytext=(0, 1),
            textcoords='offset points', ha='right', va='bottom',
            bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
            arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

    plt.show()

def calculate_matrix_dist(dataset_filenames):
    matrix = pd.DataFrame(columns=dataset_filenames.keys(), index=dataset_filenames.keys())
    all_objects = {}
    for name in dataset_filenames.keys():
        filename = dataset_filenames[name]
        all_objects[name] = get_dict_from_file(filename)
    for d1 in all_objects.keys():
        for d2 in all_objects.keys():
            same = len(set(get_names_from_files(dataset_filenames[d1])).intersection(
                set(get_names_from_files(dataset_filenames[d2]))))
            total = len(set(get_names_from_files(dataset_filenames[d1])).union(
                set(get_names_from_files(dataset_filenames[d2]))))
            different = total - same
            matrix[d1][d2] = different / total
    return matrix