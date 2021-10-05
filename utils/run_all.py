HTML('''<button id="do_run_all">Avvio esercizio</button>
<script type="text/javascript">
    var button = document.getElementById('do_run_all')
    button.addEventListener('click',hideshow,false);

    function hideshow() {
        $("#run_all_cells").click();
    }   
</script>''')
