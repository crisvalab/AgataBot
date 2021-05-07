# AgataBot

It is focused on the development of a whole spanish conversational AI model and integrating it into a **Cloud Service**, creating a very flexible and scalable API. The entire API backend is writen in Python with [Flask](https://flask.palletsprojects.com/en/1.1.x/) and other microservices are developed with [Uvicorn](https://www.uvicorn.org/). The conversational model is achieved thanks to the integration of [GPT-2](https://github.com/openai/gpt-2). It should be noted that I did the development of all this infrastructure during my internship at [Giant](http://giant.uji.es/).

Thanks to all this, you can integrate this conversational model in any of your developments with just two lines of code. Next, we can see an example with Python of how to integrate the model within your applications.

```python
import requests

while True:
    text = input("Human: ")
    r = requests.post('http://0.0.0.0:3000/agata/conversate/en/', json={"id": "1", "question": text})
    if r.status_code == 200:
        data = r.json()
        print(f'Agata: {data["answer"]}')
```

This is an example of a conversation.
```
Human: Hey! What is your name?
Agata: My name is Agata. Can I help you?
Human: Yes, I want to talk about computer science.
Agata: I have a lot of questions for you.
Human: Me too. Did you know something about C#? 
Agata: Yes, I have heard of it.
Human: What is it? 
Agata: It is a programming language that is written in C#.
Human: Ok hahaha. Do you know to code in C#?
Agata: Yes, it is the easiest programming language to learn.
Human: Where can I learn it?
Agata: The book is called "The Book of C#" and it is easy to learn.
Human: Ok I will read it. Can you recomend me other programming language?
```

### Setup 🔧

Here is an example of how to start working with **Agata Cloud**. First you will have to clone the repository and second you will have to run the setup.py file to start downloading the trained models and the heaviest files.

```shell
>>> git clone https://github.com/CristianValero/AgataBot.git
>>> python3 setup.py

>>> cd Bridge-API/
>>> python3
>>> from apiservice import db
>>> db.create_all()

>>> docker-compose up
```

Once all this process has finished ... You can now start to deploy the entire infrastructure and it would be totally ready to start working.

## Build with 🛠️

These are some of the tools that have been needed to carry out the development of AgataBot. You should also mention many of these libraries if you want to use this technology in the deployment of your project.

* [GPT-2](https://github.com/openai/gpt-2) - Main Deep Learning model
* [TensorFlow](https://www.tensorflow.org/?hl=es-419) - Framework to work with internal models
* [PyTorch](https://numpy.org/) - Framework to work with internal models
* [NumPy](https://rometools.github.io/rome/) - Used for internal maths
* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - API Python framework.
* [Uvicorn](https://www.uvicorn.org/) - Async API Python framework.

### Pre-requisites 📋

If you don't use **Docker**, you will need to **create a different environment for each microservice** that makes up the infrastructure. In addition, in each different environment you must install the different libraries so that everything works correctly. For this you can always install everything through the file **requiments.txt**.
There are some common libraries that AgataBot Cloud uses.

```
tensorflow-gpu==1.15
pytorch
numpy
flask 
flask_restful
uvicorn
```

## Authors ✒️

These are all the people who have been participating in the development of this project.

* **Cristian Valero Abundio** - *Research & Development* - [titianvalero](https://www.linkedin.com/in/cristian-valero-abundio-776646207/)

## Expresions of Gratitude 🎁

* Tell others about this project 📢
* Invite Cristian a beer 🍺 or a coffe ☕
* Share it 🤓

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
