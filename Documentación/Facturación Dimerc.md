# Descripción detallada

Existe una tabla en SAP con información sobre partidas abiertas de cuentas mayores, cada una de estas presenta una descripción, en la cual podría tener RUT, nombre de quien emite el documento, o el número de factura.

En donde la primera parte del proyecto consiste en analizar ciertas descripciones, al igual que encontrar el RUT y los números de factura, siempre y cuando estén identificados.

Siguiendo con la segunda parte del proyecto, se emplea una segunda tabla en SAP, la cual contiene partidas abiertas en este caso de deudores, donde se utilizara los RUT y los números de factura de la primera parte del proyecto. A pesar de ello, se deben realizar calces entre las partidas abiertas y el cliente, es decir, los archivos a utilizar deben ser incorporados en una carpeta llamada `input` y ser limpiados cada vez que se ejecute el programa. Luego se identifica el número de factura, siendo como requisito encontrar el match en la partida abierta uno-a-uno.

Si bien, se obtiene un RUT, se debe encontrar todas las partidas abiertas asociadas a ese RUT, a continuación se verifica si una de esas partidas puede pagar el monto indicado en la partida de la primera tabla. Si todas las partidas juntas lo hacen, o una selección específica de estas partidas. la cual suma el total del monto, se identifica un match con mayor complejidad ya que se presenta desde uno-a-muchos.

En consecuencia, se puede decir que ya existía de una lógica implementada en SAP para la realización del proyecto, sin embargo, debido a la falta de tiempo solo se logro implementa un calce de uno-a-uno respecto a los RUT en donde antes no funcionaba para todo los bancos, por lo que se solicita mejorar la propuesta anterior y ver si es posible la implementación del calce uno-a-muchos mencionado, ya que una vez realizado este procedimiento se exporta en `output` los archivos necesarios para subirlos a la plataforma SAP.