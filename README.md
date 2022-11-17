# IRS project

## About

This project is for educational purposes. The objective is to implement 3 *Information Retrieval Systems* for the final delivery. Actually there is only one model implemented, the *Classic Vector Space Model*.

If you need more info about the implementation done here please refer to this [file](Pre-entrega.md) and translate with google translate 😅

## Arquitectura del Proyecto

![Arquitectura Inicial](Project-architecture.excalidraw.svg)

## Lista de paquetes de python necesarios para el proyecto

- numpy
- matplotlib
- nltk
- jupyter

## How to run the Project

For now this project have a very simple *cli.py* file (command line interface) for ranking documents in the *Cran* collection that is already serialized in the "irs_data/Vector Space Model.pkl" file (using python pickle package).
The way of running is simple:

```shell
python cli.py
```

Note: This *cli* is simple because is not the way we want to interact with the user. In the future previous to deliver to our teachers we well create an interface in flutter that will interact with a server created in Django (this decision may change).

## Forking

Feel free to fork and do whatever you want with this code. There is nothing special here yet (and probably never because we have other projects in mind).
