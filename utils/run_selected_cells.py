from IPython.core.display import Javascript
from IPython.display import display

HTML('''<button id="do_run_sel">Avvio esercizio</button>
<script type="text/javascript">
    window.findCellIndicesByTag = function findCellIndicesByTag(tagName) {
      return (IPython.notebook.get_cells()
        .filter(
          ({metadata: {tags}}) => tags && tags.includes(tagName)
        )
        .map((cell) => IPython.notebook.find_cell_index(cell))
      );
    };

    window.runStartCells = function runStartCells() {
        var c = window.findCellIndicesByTag('run_start');
        IPython.notebook.execute_cells(c);
    };

    var button1 = document.getElementById('do_run_sel')
    button1.addEventListener('click', window.runStartCells);

</script>''')
