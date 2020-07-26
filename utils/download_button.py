html="""
<a href='./img@img_name@' download> <button>Salva immagine</button></a>
<br>
<font size="-1"><em>Puoi convenientemente produrre delle tue risposte partendo da questa stessa figura (<b>consigliato!</b>) di cui trovi l'originale nella cartella:<br> <b>@path_ex_folder@/modo_libero/img/</b>
<br>I file da tè comunque prodotti come allegati per questo esercizio in modo_libero di svolgimento devono invece essere disposti nella cartella:<br> <b>@path_ex_folder@/modo_libero/allegati/</b></em>
</font>
"""
display(HTML(html))
