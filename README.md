# AgataBot

It is focused on the development of a whole conversational AI model and integrating it into a Cloud Service, creating a very flexible and scalable API. The entire API backend is writen in Python with [Flask](https://flask.palletsprojects.com/en/1.1.x/) and other microservices are developed with [Uvicorn](https://www.uvicorn.org/). The conversational model is achieved thanks to the integration of [GPT-2](https://github.com/openai/gpt-2).

Thanks to all this, you can integrate this conversational model in any of your developments with just two lines of code. Next, we can see an example with Python of how to integrate the model within your applications.

```python
req = requests.post(url=url, json={'id': 'some id to identify conversation', 'question': 'What is your name?'})
if req.status_code == 200:
   answer = req.json()['answer']
```

It should be noted that I did the development of all this infrastructure during my internship at [Giant](http://giant.uji.es/).

## Build with 🛠️

These are some of the tools that have been needed to carry out the development of AgataBot. You should also mention many of these libraries if you want to use this technology in the deployment of your project.

* [GPT-2](https://github.com/openai/gpt-2) - Main Deep Learning model
* [TensorFlow](https://www.tensorflow.org/?hl=es-419) - Framework to work with internal models
* [PyTorch](https://numpy.org/) - Framework to work with internal models
* [NumPy](https://rometools.github.io/rome/) - Usado para generar RSS
* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - Manejador de dependencias
* [Uvicorn](https://www.uvicorn.org/) - Usado para generar RSS

### Pre-requisites 📋

If you don't use Docker, you will need to create a different environment for each microservice that makes up the infrastructure. In addition, in each different environment you must install the different libraries so that everything works correctly. For this you can always install everything through the file requiments.txt.

```
pip install gpt-2-simple
pip install tensorflow-gpu==1.15
pip install flask flask_restful
```

## Authors ✒️

These are all the people who have been participating in the development of this project.

* **Cristian Valero Abundio** - *Research & Development* - [titianvalero](https://github.com/CristianValero)

## Expresions of Gratitude 🎁

* Tell others about this project 📢
* Invite Cristian a beer 🍺 or a coffe ☕.
* Share it 🤓.

<!--### Instalación 🔧

_Una serie de ejemplos paso a paso que te dice lo que debes ejecutar para tener un entorno de desarrollo ejecutandose_

_Dí cómo será ese paso_

```
Da un ejemplo
```

_Y repite_

```
hasta finalizar
```

_Finaliza con un ejemplo de cómo obtener datos del sistema o como usarlos para una pequeña demo_

## Ejecutando las pruebas ⚙️

_Explica como ejecutar las pruebas automatizadas para este sistema_

### Analice las pruebas end-to-end 🔩

_Explica que verifican estas pruebas y por qué_

```
Da un ejemplo
```

### Y las pruebas de estilo de codificación ⌨️

_Explica que verifican estas pruebas y por qué_

```
Da un ejemplo
```

## Despliegue 📦

_Agrega notas adicionales sobre como hacer deploy_
 -->
