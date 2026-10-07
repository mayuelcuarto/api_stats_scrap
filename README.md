# API Stats Scrap

Este API se encarga de buscar un endpoint json de una web de estadísticas y a continuación rastrear los datos que se necesitan consumir, para entregar una versión resumida.

Si deseas ver en funcionamiento esta api, puedes consultar el siguiente link https://apistatsscrap.vercel.app/api/jsonScrap?games=4672313 ,
donde `?games` es el id del partido del cual obtenemos datos.

Si te interesa la documentación la podrás encontrar aquí: https://apistatsscrap.vercel.app/docs

## Entorno de ejecucióm

Si quieres reproducirla en un entorno propio, recomiendo instalar un entorno virtual de python
```bash
python -m venv venv
```

Una vez creado el entorno, deberás activarlo, suele ser mediante la ejecución en terminal de la siguiente linea:
```bash
venv\Scripts\Activate
```

Debería aparecer ``(env)`` en la terminal delante de lo que escribas, posteriormente se debe instalar fastapi, mediante el comando:
```bash
pip install fastapi uvicorn
```

Finalmente, luego de haber copiado la estructura y el codigo del proyecto o forkearlo en el tuyo, ejecutaras el comando de arranque del servidor uvicorn:
```bash
uvicorn main:app --reload
```
lo que te permitirá acceder a esta dirección en la mayoría de los casos http://127.0.0.1:8000/api/jsonScrap?games=4755392 , salvo que tu terminal asigne otro puerto.

Espero que si llegas a usarlo te ayude, se despide El Mayu.
