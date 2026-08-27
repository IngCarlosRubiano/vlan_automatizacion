# 🌐 Automatizador de Configuración de VLANs (PoC)

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Status-Prueba%20de%20Concepto-blue)
![Año](https://img.shields.io/badge/Año-2024-ff69b4)

Aplicación de escritorio en Python que automatiza la generación y el despliegue de configuraciones de VLAN en equipos Cisco, probada en entornos simulados con **GNS3**. Reduce significativamente el trabajo manual y mitiga el error humano al configurar VLANs a través de la CLI.

## 🚀 Propósito del proyecto
Diseñado como una Prueba de Concepto (PoC) para demostrar la viabilidad de la automatización de tareas de red mediante scripting en Python. El proyecto prioriza la lógica de integración de red, la validación estricta de datos y la ejecución segura de comandos remotos.

## ✨ Características
- **Gestión centralizada:** Interfaz gráfica de escritorio (Tkinter) para gestionar VLANs sin comandos manuales.
- **Conexión configurable:** Acceso por **SSH** (Paramiko) o **Telnet** (telnetlib), con host, usuario, puerto y timeout ajustables.
- **Validación de red:** Prueba de conexión independiente y validación de subred en formato CIDR (cálculo automático del gateway).
- **Despliegue automatizado:** Generación de comandos Cisco IOS (configuración tipo *router-on-a-stick*).
- **Ejecución y Monitoreo:** Configuración sobre el dispositivo vía SSH/Telnet con log de salida en tiempo real.
- **Modos Offline/Demo:** Exportación a script de texto y simulación de ejecución completa sin conexión a equipos reales.
- **Persistencia:** Guardado de configuraciones en JSON (`vlan_configs.json`).

## 🖥️ Captura de pantalla
*(Próximamente)*

## 📋 Requisitos
- Python 3.x
- [paramiko](https://pypi.org/project/paramiko/)

> ⚠️ **Nota técnica:** El módulo `telnetlib` de la librería estándar fue removido en Python 3.13. Si usas una versión reciente de Python, la conexión por Telnet requerirá una alternativa como `telnetlib3`.

## ⚙️ Instalación y uso
```bash
git clone [https://github.com/IngCarlosRubiano/vlan_automatizacion.git](https://github.com/IngCarlosRubiano/vlan_automatizacion.git)
cd vlan_automatizacion
pip install paramiko
python vlan_automation.py`
``` 

## 🛠️ Uso recomendado
Configura la conexión (IP, usuario, contraseña, protocolo y puerto) en la sección superior.

Usa Probar Conexión para verificar el acceso antes de aplicar cambios.

Agrega las VLANs necesarias (ID, nombre y subred) en la tabla.

Usa Modo Demo para simular la ejecución, o Ejecutar Automatización para aplicar la configuración.

## 👤 Autor
# Carlos Rubiano

<p>
<a href="https://github.com/IngCarlosRubiano/IngCarlosRubiano" target="_blank">
<img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"/>
</a>
<a href="https://www.linkedin.com/in/carlos-rubiano-engineer/" target="_blank">
<img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white"/>
</a>
</p>


⭐ Si este proyecto te fue útil, no olvides dejar una estrella.