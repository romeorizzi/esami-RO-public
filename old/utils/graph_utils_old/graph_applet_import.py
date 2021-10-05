from IPython.core.display import display, HTML, Markdown, clear_output, Javascript
from string import Template
import pandas as pd
import json, random
import yaml
import copy
import networkx as nx
import math
import xml.etree.ElementTree as ET
import ipywidgets as widgets
import os
import time
import os.path
from os import path as p
import glob
from datetime import datetime
from IPython.core.display import display, HTML, Markdown, clear_output, Javascript
import ipywidgets as widgets
HTML('''
<script src="../../graph_utils/js/sigma.min.js"></script>
<script src="../../graph_utils/js/sigma.plugins.dragNodes.js"></script>
<script src="../../graph_utils/js/sigma.canvas.edges.labels.curvedArrow.js"></script>
<script src="../../graph_utils/js/sigma.canvas.edges.curvedArrow.js"></script>
<script src="../../graph_utils/js/sigma.canvas.edges.curve.js"></script>
<script src="../../graph_utils/js/sigma.canvas.edges.labels.curve.js"></script>
<script src="../../graph_utils/js/sigma.canvas.edges.labels.def.js"></script>
<script src="../../graph_utils/js/sigma.exporters.svg.js"></script>
<script src="../../graph_utils/js/settings.js"></script>
<script src="../../graph_utils/js/sigma.renders.snapshots.js"></script>
''')