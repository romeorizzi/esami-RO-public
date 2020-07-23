from IPython.core.display import Javascript
from IPython.display import display

HTML('''
     <button id="do_reload_sel">Ricarica</button>
<script type="text/javascript">
    window.findCellIndicesByTag = function findCellIndicesByTag(tagName) {
      return (IPython.notebook.get_cells()
        .filter(
          ({metadata: {tags}}) => tags && tags.includes(tagName)
        )
        .map((cell) => IPython.notebook.find_cell_index(cell))
      );
    };

    window.reloadCells = function reloadCells() {
        var c = window.findCellIndicesByTag('reload');
        IPython.notebook.execute_cells(c);
    };
    var button2 = document.getElementById('do_reload_sel')
    button2.addEventListener('click', window.reloadCells);

</script>''')
