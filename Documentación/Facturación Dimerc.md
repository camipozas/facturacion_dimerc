Descripción detallada:
Existe una tabla en SAP con información sobre partidas abiertas de cuentas mayores.
Cada una de estas partidas abiertas tiene una descripción, que podría tener el RUT de
quien emite el documento, o el número de factura.

La primera parte del proyecto es analizar esas descripciones y encontrar los RUTs y
números de factura, en caso de existir.

Para la segunda parte, se debe usar una segunda tabla en SAP, la cual también contiene
partidas abiertas, pero esta vez de deudores. Usando los RUTs y los números de factura
de la primera parte, se deben realizar calces entre las partidas abiertas:
> Los archivos a utilizar deben ser incorporados en `input` y ser limpiados cada vez que se ejecute.
- Si se tiene un número de factura, se debe encontrar la partida abierta que tenga ese
número. Este es un match sencillo, uno-a-uno.

- Si se tiene un RUT, se debe encontrar todas las partidas abiertas asociadas a ese RUT.
Luego, se debe ver si una de esas partidas puede pagar el monto indicado en la partida
de la primera tabla, o si todas las partidas juntas lo hacen, o quizás una selección
específica de estas partidas suma en total ese monto. Este es un match más complejo,
uno-a-muchos.

Originalmente ya existía una lógica implementada en SAP para realizar esto. Sin embargo,
debido a falta de tiempo, solo se pudo implementar un calce uno-a-uno respecto a los
RUTs, por lo que se solicita mejorar la propuesta anterior y ver si es posible
implementar ese calce uno-a-muchos mencionado.

Una vez realizado lo anterior se exportan en `output` los archivos necesarios para subirlos a SAP.
