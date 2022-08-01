Lógica de reconocimiento de RUT
-------------------------------
Librerías usadas: re

1. Buscar patrones de la forma XXXXXXXX o XX.XXX.XXX, que empiecen con
   un dígito distinto de 0
	- Regex: r"[1-9]\d{7}|[1-9]\d\.\d{3}\.\d{3}"

2. Si no hay resultados, buscar patrones de la forma XXXXXXX o X.XXX.XXX,
   que empiecen con un dígito distinto de 0
	- Regex: r"[1-9]\d{6}|[1-9]\.\d{3}\.\d{3}"

3. ES IMPORTANTE QUE (1) Y (2) SE HAGAN POR SEPARADO Y EN ESE ORDEN. Al menos en
   mi caso, si intento hacer todo a la vez, los patrones de (1) "bloquean" los
   patrones de (2) y pierdo información valiosa

4. A partir de los resultados, calcular el dígito verificador

5. Ver si, inmediatamente después del patrón encontrado en el texto, hay un
   número, que puede o no estar precedido por un guion, y ver si coincide
   con el dígito verificador. Para eso, combinar el patrón encontrado con
   el posible guion y el dígito verificador encontrado
	- Regex: <<patrón>> + r"-?" + <<DV>>

6. Nota: si el dígito verificador es K, también estoy considerando la posibilidad
   de que esté en minúsculas. En ese caso, el patrón sería:
	- Regex: <<patrón>> + r"-?[kK]"

7. Si todo eso coincide, entonces se encontró un RUT