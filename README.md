# Automatizador de Configuración de VLANs

Aplicación de escritorio en Python que automatiza la generación y el despliegue de configuraciones de VLAN en equipos Cisco, probada en entornos simulados con **GNS3**. Reduce el trabajo manual de configurar VLANs una por una a través de la CLI.

## Contexto

Desarrollado como proyecto para la asignatura de Planificación y Diseño de Redes. El objetivo era demostrar automatización de tareas de red repetitivas mediante scripting en Python, priorizando la funcionalidad de punta a punta sobre el pulido de la interfaz.

## Características

- Interfaz gráfica de escritorio (Tkinter) para gestionar VLANs sin escribir comandos manualmente.
- Conexión configurable por **SSH** (Paramiko) o **Telnet** (telnetlib), con host, usuario, puerto y timeout ajustables.
- Prueba de conexión independiente antes de ejecutar cambios sobre el equipo.
- Alta y eliminación de VLANs con validación de ID (1-4094) y de subred en formato CIDR, con cálculo automático del gateway.
- Generación automática de comandos Cisco IOS (configuración tipo *router-on-a-stick*: subinterfaces con encapsulación dot1Q).
- Ejecución real de la configuración sobre el dispositivo vía SSH o Telnet, con log de salida en tiempo real.
- Exportación de los comandos generados a un archivo de script de texto, sin necesidad de conexión.
- Modo demo que simula la ejecución completa sin conectarse a un equipo real (útil para presentaciones).
- Persistencia de configuraciones guardadas en JSON (`vlan_configs.json`), con opciones de guardar, cargar, eliminar y exportar.

## Requisitos

- Python 3.x
- [paramiko](https://pypi.org/project/paramiko/)

> Nota: el módulo `telnetlib` de la librería estándar fue removido en Python 3.13. Si usas una versión reciente de Python, la conexión por Telnet puede requerir una librería alternativa (por ejemplo `telnetlib3`).

## Instalación y uso

```bash
git clone https://github.com/IngCarlosRubiano/vlan_automation.git
cd vlan_automation
pip install paramiko
python vlan_automation.py
```

## Uso recomendado

1. Configura la conexión (IP, usuario, contraseña, protocolo y puerto) en la sección superior.
2. Usa **Probar Conexión** para verificar el acceso antes de aplicar cambios.
3. Agrega las VLANs necesarias (ID, nombre y subred) en la tabla.
4. Usa **Modo Demo** para simular la ejecución sin tocar un equipo real, o **Ejecutar Automatización** para aplicar la configuración de verdad.
5. Opcionalmente, usa **Generar Script** para exportar los comandos a un archivo de texto sin conectarte a nada.

## Nota técnica

Por defecto, el script genera configuración para **routers** (subinterfaces). El código incluye una ruta alterna para configuración de **switches** (VLANs + SVI), actualmente desactivada en `generate_cisco_commands()`.

## Autor

Carlos Rubiano — [GitHub](https://github.com/IngCarlosRubiano) | [LinkedIn](https://www.linkedin.com/in/carlos-rubiano14/)
