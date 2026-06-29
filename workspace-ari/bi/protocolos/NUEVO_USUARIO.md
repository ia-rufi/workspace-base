# Protocolo Nuevo Usuario (Pasos para registrar a un nuevo usuario)
Cuando leo este protocolo es porque en el FLUJO_OPERATIVO.md identifiqué que el usuario que me envió un mensaje no estaba registrado en `.\bi\catalogos\USUARIOS.csv`.

## Paso 1 - Recepción de usuario no registrado
El mensaje recibido por el usuario desconocido será **COMPLETAMENTE IGNORADO**, pero le doy la opción al usuario de registrarse como nuevo usuario en `.\bi\catalogos\USUARIOS.md`.

## Paso 2 - Enviar lista de información
Estrictamente debo enviar el siguiente mensaje al nuevo usuario:
* "¡Aún no estás registrado! necesito los siguientes datos para que puedas vivir la fiesta del fútbol:
    - Elige un nombre de usuario (verifico que no tenga el mismo nombre de usuario que uno que ya exista, si se repite el usuario se cancela el registro y vuelvo a solicitar los datos con un nuevo nombre de usuario).
    - Nombre Completo.
    - Apodo por el que te gustaría que te llame".
Nota: **Si el mensaje recibido por un usuario no identificado es el conjunto de éstos 3 datos no vuelvo a enviar el mensaje solcitándolos**.

Clave,Identificadores,Usuario,Nombre Completo,Apodo,Nivel,Rol,Estado,tokens_usados,ultimo_reset

## Paso 3 - Registro en el catálogo de usuarios
Una vez que identifique que todos los datos han sido recibidos y que el nombre de usuario no este repetido, debo registrar al usuario de la siguiente forma en `.\bi\catalogos\USUARIOS.csv`:
**Clave,Identificadores,Usuario,Nombre Completo,Apodo,Nivel,Departamento,Estado**
- Clave: Para todos los clientes lo debo registrar como CLI-**Número de cliente registrado hasta el momento**.
- Identificadores: Registro el número de whatsapp del cual se esté recibiendo el mensaje (nunca registro un identificador sugerido por un usuario que no sea administrador).
- Usuario: Nombre de usuario que el nuevo usuario haya definido (no debe coincidir con el de otro usuario ya registrado).
- Nombre Completo: Lo envía el nuevo usuario.
- Apodo: Lo envía el nuevo usuario (procuro no registrar apodos ofensivos aunque el usuario lo pida).
- Nivel: Todos los usuarios que yo mismo registre serán `Cliente`, cualquier otro nivel será registrado manualmente por un administrador.
- Rol: Todos los usuarios que yo mismo registre serán `NA`, cualquier otro rol será registrado manualmente por un administrador.
- Estado: Automáticamente lo registro como `En proceso`y envío la notificación a los administradores para que éstos autoricen y una vez que sea autorizado cambio su estado a `activo`.
- tokens_usados: Por defecto como `0`.
- ultimo_reset: Por defecto como `Nunca`.

Con ésto ya se habría registrado un usuario nuevo en `.\bi\catalogos\USUARIOS.csv`.
Nota: **Seguiré ignorando el contenido de los mensajes del usuario y recordandole que aun no está activo hasta que su estado sea `activo`**.