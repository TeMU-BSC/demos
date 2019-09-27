# demos-deploy
Dockerized deployment of the BSC Text Mining unit demos


/////////////////////

# ENTRYPOINT del Dockerfile https://github.com/PlanTL-SANIDAD/SPACCC_POS-TAGGER/blob/master/Dockerfile

analyze --flush -f /config/config.cfg --ftok /config/tokenizer.dat --fsplit /config/splitter.dat --floc /config/singlewords.dat --usr --fmap /config/usermap.dat --noquant


# Consejos de Sergio sergio.mendoza@bsc.es sobre el SPACCC de felipe:
conseguir que corra flask en ubuntu 12
si no funciona, alternativa: web.py (simple sencillo)

posible trampa: desde el contenedor de SPACCC, poner a correr analyzer como servicio y ???