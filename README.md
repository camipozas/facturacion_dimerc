# Match de abonos en SAP

### Español
## Contexto
Hay clientes que no suelen pagar la totalidad del monto sino que lo hacen por partes. Hasta antes de la solución esto se hacía uno a uno.

## Solución
Realizar una herramienta que permita reconocer y realizar calces de distintos documentos, relacionados a un número de factura. La descripción detallada del proceso se encuentra [aquí](Documentación/Facturación%20Dimerc.md). Además, se implementó una [lógica de reconocimiento de rut](Documentación/Lógica%20RUT.md).
> Cabe destacar que esta solución es válida para todas las sociedades de un holding.

Si bien, el código de por si era bueno. Se necesitaba pensar en la ejecución continua y en el usuario final, el cual no está acostumbrado/a a los códigos, así como también instalar dependencias. En primera instancia se pensó en utilizar [Docker](https://docs.docker.com/engine/install/) junto con Realpath: [Linux](https://zoomadmin.com/HowToInstall/UbuntuPackage/realpath) - [macOS](https://ports.macports.org/port/realpath/) para el manejo de archivos. Sin embargo, los usuarios ocupan Windows en el día a día, es por esto que se utilizó [autopy-py-to-exe](https://pypi.org/project/auto-py-to-exe/) el cual funciona de manera análoga a lo anteriormente mencionado. 

Dicho lo anterior, para su ejecución es necesario realizar lo siguiente:
1. Tener una carpeta en donde se alojará el archivo `main.exe`
2. Una vez en el directorio, crear la carpeta `input` y `output`, en `input` se agregan los archivos iniciales para su ejecución, cabe destacar que estos deben ser limpiados cada vez que es vaya a ejecutar. Por otro lado, en la carpeta `output` se guarda un histórico de archivos generados. No es necesario hacer cambios en esta última.
3. Si no es la primera vez que ejecuta, no repetir pasos 1 y 2.

> Para mayor orden se recomienda una carpeta exclusiva donde se realizan los pasos anteriormente mencionados.

--------
### English
## Context
There are clients who do not usually pay the entire amount but do so in parts. Until before the solution this was done one by one.

## Solution
Create a tool that allows recognizing and matching different documents, related to an invoice number. The detailed description of the process can be found [here](Documentation/Billing%20Dimerc.md). In addition, a [route recognition logic](Documentation/Logic%20RUT.md) was implemented.
> It should be noted that this solution is valid for all the companies of a holding company.

Although, the code itself was good. It was necessary to think about continuous execution and the end user, who is not used to code, as well as installing dependencies. It was first thought to use [Docker](https://docs.docker.com/engine/install/) together with Realpath: [Linux](https://zoomadmin.com/HowToInstall/UbuntuPackage/realpath) - [ macOS](https://ports.macports.org/port/realpath/) for file handling. However, users occupy Windows on a daily basis, that is why [autopy-py-to-exe](https://pypi.org/project/auto-py-to-exe/) was used, which It works analogously to the above.

That said, for its execution it is necessary to do the following:
1. Have a folder where the `main.exe` file will be located
2. Once in the directory, create the `input` and `output` folders, in `input` the initial files are added for its execution, it should be noted that these must be cleaned each time it is going to be executed. On the other hand, a history of generated files is saved in the `output` folder. It is not necessary to make changes to the latter.
3. If it is not the first time you run, do not repeat steps 1 and 2.

> For greater order, an exclusive folder is recommended where the aforementioned steps are carried out.