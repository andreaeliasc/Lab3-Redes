# Laboratorio 3 - Algoritmos de enrutamiento 

## Objetivos
- Conocer los algoritmos de enrutamiento utilizados en las implementaciones actuales de Internet.
- Comprender cómo funcionan las tablas de enrutamiento.

## Algoritmos implementados
- [x] Flooding
- [x] Distance Vector Routing
- [x] Link State Routing

## Requerimientos
Las herramientas usadas para el desarrollo y uso del programa fueron:
```sh
Python 3.7+
Slixmpp 1.7.1
aioconsole 0.3.2
aiodns 3.0.0
cffi 1.14.6
cycler 0.10.0
kiwisolver 1.3.2
matplotlib 3.4.3
networkx 2.6.2
numpy 1.21.2
Pillow 8.3.1
pkg_resources 0.0.0
pyasn1 0.4.8
pyasn1-modules 0.2.8
pycares 4.0.0
pycparser 2.20
pyparsing 2.4.7
python-dateutil 2.8.2
PyYAML 5.4.1
six 1.16.0
```
Puedes instalarlas usando el siguiente comando:
```sh
pip install -r requirements.txt 
```
En caso de que `aioconsole` no se haya instalado por no encontrar una versión adecuada o algún error, prueba usando el siguiente comando:
```
pip install --upgrade setuptools
```
Luego, instala `aioconsole` de manera individual usando pip, de la siguiente forma:
```
pip install aioconsole
```

## Getting Started
```sh
python main.py
```
Cuando solicite el archivo de nombres, ingresar `names.txt`, y para el nombre del archivo con la topología, colocar `topology.txt`
## Autores
Andrea Elías https://github.com/andreaeliasc
Diego Estrada https://github.com/diegoestradaXO
Luis Urbina https://github.com/virtualmonkey
