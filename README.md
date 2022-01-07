# Rutificainador
Script en Python3 que permite buscar información en base a un RUT Chileno en la pagina https://www.nombrerutyfirma.com mas conocida como Rutificador


# Instalacion
```bash
git clone https://github.com/MikuWRS/Rutificainador
cd Rutificainador
pip install -r requirements.txt
```

# Modo de uso

```bash
python3 rutificainador.py -comandos "rut"
```
Comandos:
- -r Rut
- -l Lista de Ruts
- -e Exportar en csv
- -h Help

Formato del rut:
- 11.222.333-0
El digito verificador puede ser K o k, sin embargo se autoreemplazara por un 0.
Si no sabes el digito, puedes reemplazarlo por un 0 igualmente.

Ejemplo
```bash
python3 rutificainador.py -r "11.222.333-0" -e
python3 rutificainador.py -l ruts.txt -e
```
