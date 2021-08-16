# Laboratorio 1 - Tópicos Especiales en Telemática: Sockets
Repositorio con todo lo necesario para completar el Laboratorio 1 de Tópicos Especiales en Telemática - 2021-2

- [Laboratorio 1 - Tópicos Especiales en Telemática: Sockets](#laboratorio-1---tópicos-especiales-en-telemática-sockets)
  - [Estructura](#estructura)
  - [Instrucciones de uso](#instrucciones-de-uso)
  - [Ejemplo](#ejemplo)
  - [Información adicional](#información-adicional)

## Estructura
Esta aplicación tiene cuatro componentes principales:
* *Client*: el cliente, desarrollado en Python, que se conecta por medio de un socket TCP a el Reader (que se describe más abajo). El cliente es un programa sencillo que recibe texto escrito por el usuario, verifica que no esté vacío, y lo envía al Reader, que luego lo verificará, por medio del socket.
* *Reader*: este es el servidor con el que el cliente tiene contacto directo. Es un servicio desarrollado en Python, que corre en el puerto 50000. Su función es recibir el mensaje del cliente y verificar que sea váliddo. Un mensaje válido es aquel que solamente consta de letras, sin espacios, números u otros caracteres especiales. Si el mensaje es válido, el Reader enviará el mensaje por otra conexión por socket hacia el Capitalizer, que luego lo enviará al Reverser y, finalmente, el Reader entregará la respuesta del Reverser al cliente. El Reader tiene un protocolo que está definido de la siguiente manera:
  * 10 - QUIT: si el cliente desea salir y cerrar la conexión (lo cual hace enviando '0'). Este código es retornado al cliente para confirmar que el cierre de la conexión fue exitoso por instrucción del cliente.
  * 20 - INVALID CHARACTERS: si el mensaje del cliente contiene algún caracter no válido, el Reader le retorna esta respuesta por el socket al cliente, que significa que el mensaje contiene caracteres inválidos.
  * 30 - MSG OK: si el mensaje del cliente es válido, el Reader retorna al cliente este código y procede a enviar el mensaje al Capitalizer (descrito a continuación).
* *Capitalizer*: este es un servicio ubicado en otro servidor en el puerto 50001 y desarrollado en Java. Este servicio se conecta por medio de un socket TCP con el Reader y recibe los mensajes que el Reader le manda, para proceder a convertirlos en mensajes escritos en mayúsculas (ejemplo: hello -> HELLO), que luego envía al Reverser (que se describe más abajo). Luego recibe la respuesta del Reverser y se la envía al Reader, para que éste a su vez se la pueda enviar al cliente, todo por medio de sockets. El protocolo de respuestas del Capitalizer está definido de la siguiente manera:
  * 10 - QUIT: igual que en el Reader, este código se retorna cuando se ha cerrado exitosamente la conexión por instrucción del cliente.
  * 40 - MSG OK: este es el código de éxito del Capitalizer, que le retorna al Reader que el mensaje fue exitosamente convertido a mayúsculas y se enviará al Reverser. (_Nota_: es importante destacar que este servicio ya no necesita tener un componente tan importante de error handling para los mensajes del cliente, ya que el Reader los filtró previamente antes de enviarlos aquí).
* *Reverser*: este es el último servicio, que está en un tercer servidor en el puerto 50002 y está desarrollado en NodeJS. El Capitalizer se conecta a este servicio por medio de un socket y envía el mensaje en mayúsculas, que luego el Reverser procede a invertir (ejemplo: HELLO -> OLLEH) y lo retorna al Capitalizer por el socket, que a su vez lo retorna al Reader y luego este al cliente. El protocolo está definido de la siguiente manera:
  * 10 - QUIT: como en el Reader y el Capitalizer, este código se retorna cuando se ha cerrado exitosamente la conexión por instrucción del cliente.
  * 50 - MSG OK: este código se retorna cuando el mensaje ha sido correctamente reversado.

## Instrucciones de uso
En este momento hay tres instancias de EC2 en AWS, cada una con uno de los tres servicios mencionados anteriormente. A agosto 16, 2021, la información de los servidores es la siguiente:
* Reader
  * IP Pública: 34.200.255.172
  * DNS: ec2-34-200-255-172.compute-1.amazonaws.com
* Capitalizer
  * IP Pública: 44.197.245.190
  * DNS: ec2-44-197-245-190.compute-1.amazonaws.com
* Reverser
  * IP Pública: 3.239.0.55
  * DNS: ec2-3-239-0-55.compute-1.amazonaws.com

Para correr el cliente, correr el comando python \<_ruta a client.py_\>. Esto conectará el cliente con el Reader, por medio de un socket, luego el Reader con el Capitalizer, por medio de otro socket y luego el Capitalizer con el reverser, por medio de otro socket. Aquí, el cliente le pedirá al usuario ingresar un mensaje, que puede contener solamente caracteres a-z o A-Z, o que ingrese '0' para salir. Cualquier otro mensaje, que no siga esta estructura o que no sea el mensaje de salida, generará un código 20 - INVALID CHARACTERS por parte del Reader. Por el contrario, si el mensaje es válido, el usuario verá el código 30 - MSG OK -> \<mensaje que escribió\> y luego el resultado final del Reverser, que será 50 - MSG OK -> \<mensaje en mayúsculas y reversado\>.

## Ejemplo

* Client

  ![plot](Example%20Images/client-example.png)

* Reader
  
  ![plot](Example%20Images/reader-example.png)

* Capitalizer
  
  ![plot](Example%20Images/capitalizer-example.png)

* Reverser
  
  ![plot](Example%20Images/reverser-example.png)


## Información adicional

* Este es un sistema distribuido y las conexiones entre cualquier par de servicios funcionan como una arquitectura cliente/servidor separada. Por ejemplo, entre Client y Reader hay una arquitectura cliente/servidor en la que Client es el cliente y Reader es el servidor. Entre Reader y Capitalizer también hay una arquitectura cliente/servidor en la que Reader es el cliente y Capitalizer es el servidor. Entre Capitalizer y Reverser también hay una arquitectura cliente/servidor en la que el Capitalizer es el cliente y el Reverser el servidor.
* Para la conexión por sockets se usaron sockets TCP, principalmente debido a que se quería garantizar la entrega de los datos a cada servicio, sin pérdida de datos, y para no tener que implementar protocolos de reenvío y confiabilidad manualmente. Adicionalmente, todos los servicios que actúan como clientes en este caso esperan una respuesta y no se quiere que otros mensajes interfieran con estos en el proceso, lo cual implica que TCP era una mejor opción que UDP en este caso.
* Todos los servidores están diseñados para soportar varios clientes. El Reader y el Capitalizer ambos tienen funcionalidad de multithreading, en la que se abre un hilo diferente para atender a cada cliente nuevo y el Reverser es basado en eventos, y responde a cada mensaje a medida que le llega, sin necesidad de bloquearse, lo cual implica que no es necesario un diseño explícito de hilos para el Reverser, ya que esta funcionalidad de eventos la provee NodeJS.
* En las tres instancias EC2 de AWS en las que están el Reader, Capitalizer y Reverser, se usó PM2 para la gestión de procesos, para correrlos como daemon en segundo plano y mantenerlos activos.