# AgataBot

It is focused on the development of a whole conversational AI model and integrating it into a Cloud Service, creating a very flexible and scalable API. The entire API backend is writen in Python with [Flask](https://flask.palletsprojects.com/en/1.1.x/) and other microservices are developed with [Uvicorn](https://www.uvicorn.org/). The conversational model is achieved thanks to the integration of [GPT-2](https://github.com/openai/gpt-2) through the [GPT-2-Simple](https://github.com/minimaxir/gpt-2-simple) library.

Thanks to all this, you can integrate this conversational model in any of your developments with just two lines of code. Next, we can see an example with Python of how to integrate the model within your applications.

```
req = requests.post(url=url, json={'id': 'some id to identify conversation', 'question': 'What is your name?'})
if req.status_code == 200:
   sentence_to_en = req.json()['answer']
```

It should be noted that I did the development of all this infrastructure during my internship at [Giant](http://giant.uji.es/).

## Starting 🚀

These instructions will allow you to get a copy of the project running on your local machine for development and testing purposes.

See **Deployment** to know how to deploy the project.

### Pre-requisites 📋

You need to install these libraries for everything to work or, failing that, deploy the infrastructures through Docker.

```
pip install gpt-2-simple
pip install tensorflow-gpu==1.15
pip install flask flask_restful
```

## Authors ✒️

These are all the people who have been participating in the development of this project.

* **Cristian Valero Abundio** - *Research & Development* - [titianvalero](https://github.com/CristianValero)

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

## Construido con 🛠️

_Menciona las herramientas que utilizaste para crear tu proyecto_

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - El framework web usado
* [Maven](https://maven.apache.org/) - Manejador de dependencias
* [ROME](https://rometools.github.io/rome/) - Usado para generar RSS

## Contribuyendo 🖇️

Por favor lee el [CONTRIBUTING.md](https://gist.github.com/villanuevand/xxxxxx) para detalles de nuestro código de conducta, y el proceso para enviarnos pull requests.

## Wiki 📖

Puedes encontrar mucho más de cómo utilizar este proyecto en nuestra [Wiki](https://github.com/tu/proyecto/wiki)

## Versionado 📌

Usamos [SemVer](http://semver.org/) para el versionado. Para todas las versiones disponibles, mira los [tags en este repositorio](https://github.com/tu/proyecto/tags).

## Licencia 📄

Este proyecto está bajo la Licencia (Tu Licencia) - mira el archivo [LICENSE.md](LICENSE.md) para detalles

## Expresiones de Gratitud 🎁

* Comenta a otros sobre este proyecto 📢
* Invita una cerveza 🍺 o un café ☕ a alguien del equipo. 
* Da las gracias públicamente 🤓.
* etc.



---
⌨️ con ❤️ por [Villanuevand](https://github.com/Villanuevand) 😊 -->
