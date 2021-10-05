## Sottosequenze ##

### Valori possibili per seq_type: ###
- 'SC': strettamente crescente;
- 'ND': non decrescente;
- 'SD': strettamente decrescente;
- 'NC': non-crescente;
- 'V': prima giù, poi su;
- 'A': prima su, poi giù;
- 'SV': prima strettamente giù, poi strettamente su;
- 'SA': prima strettamente su, poi strettamente giù;
- 'ZigZag': primo passo a crescere e poi alterna a ogni passo;
- 'ZagZig': primo passo a calare e poi alterna a ogni passo;
- 'ZigZagEQ': primo passo a crescere e poi alterna ad ogni passo, con valori consecutivi che possono essere uguali;
- 'ZagZigEQ': primo passo a calare e poi alterna ad ogni passo, con valori consecutivi che possono essere uguali.

### Procedure del verificatore a disposizione ###
- __is_subseq(s, subs)__: verifica se subs è sottosequenza di s.
- __is_seq_of_type(s, name_s, seq_type)__: valuta se la sequenza di interi _s_, di nome _name_s_, è di tipo seq_type. Valore di ritorno (bool, NO_cert_string): in caso affermativo, il bool ritornato come prima componente è True e la seconda componente è None; altrimenti il bool è False e viene restituita una stringa che riporta una violazione puntuale alla proprietà richiesta.
- __is_subseq_of_type(s, name_s, subs, name_subs, subs_type, pt_green, pt_red, forced_ele_pos = None, start_banned_interval = None, end_banned_interval = None)__: verifica se subs, una sequenza di interi di nome _name_subs_, è sequenza di tipo _subs_type e sottosequenza della sequenza s:
    - Se forced_ele_pos != None è richiesto che subs contenga l'elemento s[forced_ele_pos];
    - Se start_banned_interval, end_banned_interval != None è richiesto che subs eviti il sottointervallo bandito di s;
    Valore di ritorno: una stringa contenente la valutazione del certificato subs immesso dallo studente, a tale scopo i parametri pt_green e pt_red_ mentre pt_blue = pt_red - pt_green è fatto implicito.
- __eval_coloring(s, name_s, col, name_col, subs_type, pt_green=2, pt_red=15)__: verifica se col, una sequenza di interi positivi di nome name_col, offra una colorazione degli elementi nella sequenza s, di nome name_s, tale che restringendo l'attenzione ai soli elementi di qualsivoglia colore, la sottosequenza di essi sia sequenza di tipo subs_type. Valore di ritorno: una stringa contenente la valutazione del certificato col immesso dallo studente, a tale scopo i parametri pt_green e pt_red mentre pt_blue = pt_red - pt_green è fatto implicito.
