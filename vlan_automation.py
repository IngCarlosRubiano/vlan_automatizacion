#!/usr/bin/env python3
"""
Automatizador de Configuración de VLANs
Para Planificación y Diseño de Redes 2025
Autor: Sistema de Automatización de Redes
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog, simpledialog
import json
import paramiko
import telnetlib
import time
from datetime import datetime
import ipaddress
import os

class VLANAutomator:
    def __init__(self, root):
        self.root = root
        self.root.title("Automatizador de VLANs - GNS3")
        self.root.geometry("1100x750")
        self.root.resizable(True, True)
        self.root.minsize(900, 600)
        
        # Variables
        self.configurations = []
        self.current_config = None
        self.config_file = "vlan_configs.json"
        
        # Cargar configuraciones guardadas
        self.load_configurations()
        
        # Crear interfaz
        self.create_widgets()
        
    def create_widgets(self):
        # Canvas principal con scrollbar
        canvas = tk.Canvas(self.root)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Habilitar scroll con rueda del mouse
        self.enable_mousewheel(canvas)
        
        # Frame principal
        main_frame = ttk.Frame(scrollable_frame, padding="10")
        main_frame.pack(fill="both", expand=True)
        
        # Título
        title = ttk.Label(main_frame, text="🌐 Automatizador de VLANs para GNS3", 
                         font=('Arial', 16, 'bold'))
        title.pack(pady=10)
        
        # Sección de Conexión
        conn_frame = ttk.LabelFrame(main_frame, text="Conexión al Dispositivo", padding="10")
        conn_frame.pack(fill="x", pady=5)
        
        # Fila 1
        row1 = ttk.Frame(conn_frame)
        row1.pack(fill="x", pady=2)
        
        ttk.Label(row1, text="IP/Host:", width=12).pack(side="left", padx=2)
        self.host_entry = ttk.Entry(row1, width=15)
        self.host_entry.pack(side="left", padx=2)
        self.host_entry.insert(0, "192.168.1.1")
        
        ttk.Label(row1, text="Usuario:", width=10).pack(side="left", padx=2)
        self.user_entry = ttk.Entry(row1, width=12)
        self.user_entry.pack(side="left", padx=2)
        self.user_entry.insert(0, "admin")
        
        ttk.Label(row1, text="Contraseña:", width=10).pack(side="left", padx=2)
        self.pass_entry = ttk.Entry(row1, width=12, show="*")
        self.pass_entry.pack(side="left", padx=2)
        self.pass_entry.insert(0, "admin")
        
        # Fila 2
        row2 = ttk.Frame(conn_frame)
        row2.pack(fill="x", pady=2)
        
        ttk.Label(row2, text="Protocolo:", width=12).pack(side="left", padx=2)
        self.protocol_var = tk.StringVar(value="Telnet")
        ttk.Radiobutton(row2, text="SSH", variable=self.protocol_var, 
                       value="SSH").pack(side="left", padx=2)
        ttk.Radiobutton(row2, text="Telnet", variable=self.protocol_var, 
                       value="Telnet").pack(side="left", padx=2)
        
        ttk.Label(row2, text="Puerto:", width=8).pack(side="left", padx=2)
        self.port_entry = ttk.Entry(row2, width=8)
        self.port_entry.pack(side="left", padx=2)
        self.port_entry.insert(0, "23")
        
        ttk.Label(row2, text="Timeout (seg):", width=12).pack(side="left", padx=2)
        self.timeout_entry = ttk.Entry(row2, width=8)
        self.timeout_entry.pack(side="left", padx=2)
        self.timeout_entry.insert(0, "30")
        
        # Sección de Configuraciones
        config_frame = ttk.LabelFrame(main_frame, text="Gestión de Configuraciones", padding="10")
        config_frame.pack(fill="x", pady=5)
        
        config_row = ttk.Frame(config_frame)
        config_row.pack(fill="x")
        
        ttk.Label(config_row, text="Configuración:", width=12).pack(side="left", padx=2)
        self.config_combo = ttk.Combobox(config_row, width=25, state="readonly")
        self.config_combo.pack(side="left", padx=2)
        self.config_combo.bind("<<ComboboxSelected>>", self.load_selected_config)
        self.update_config_list()
        
        ttk.Button(config_row, text="➕ Nueva", 
                  command=self.new_configuration).pack(side="left", padx=2)
        ttk.Button(config_row, text="💾 Guardar", 
                  command=self.save_configuration).pack(side="left", padx=2)
        ttk.Button(config_row, text="🗑️ Eliminar", 
                  command=self.delete_configuration).pack(side="left", padx=2)
        ttk.Button(config_row, text="📂 Exportar", 
                  command=self.export_configuration).pack(side="left", padx=2)
        
        # Sección de VLANs
        vlan_frame = ttk.LabelFrame(main_frame, text="Configuración de VLANs", padding="10")
        vlan_frame.pack(fill="both", expand=True, pady=5)
        
        # Controles para agregar VLANs
        control_row = ttk.Frame(vlan_frame)
        control_row.pack(fill="x", pady=5)
        
        ttk.Label(control_row, text="VLAN ID:", width=10).pack(side="left", padx=2)
        self.vlan_id_entry = ttk.Entry(control_row, width=8)
        self.vlan_id_entry.pack(side="left", padx=2)
        
        ttk.Label(control_row, text="Nombre:", width=8).pack(side="left", padx=2)
        self.vlan_name_entry = ttk.Entry(control_row, width=15)
        self.vlan_name_entry.pack(side="left", padx=2)
        
        ttk.Label(control_row, text="Subred:", width=8).pack(side="left", padx=2)
        self.subnet_entry = ttk.Entry(control_row, width=18)
        self.subnet_entry.pack(side="left", padx=2)
        self.subnet_entry.insert(0, "192.168.1.0/24")
        
        ttk.Button(control_row, text="➕ Agregar VLAN", 
                  command=self.add_vlan).pack(side="left", padx=5)
        
        # Tabla de VLANs
        tree_frame = ttk.Frame(vlan_frame)
        tree_frame.pack(fill="both", expand=True, pady=5)
        
        tree_scroll = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        
        self.vlan_tree = ttk.Treeview(tree_frame, columns=("ID", "Nombre", "Subred", "Gateway"), 
                                      show="headings", height=6, yscrollcommand=tree_scroll.set)
        
        tree_scroll.config(command=self.vlan_tree.yview)
        
        self.vlan_tree.heading("ID", text="VLAN ID")
        self.vlan_tree.heading("Nombre", text="Nombre")
        self.vlan_tree.heading("Subred", text="Subred")
        self.vlan_tree.heading("Gateway", text="Gateway")
        
        self.vlan_tree.column("ID", width=80)
        self.vlan_tree.column("Nombre", width=150)
        self.vlan_tree.column("Subred", width=150)
        self.vlan_tree.column("Gateway", width=150)
        
        self.vlan_tree.pack(side="left", fill="both", expand=True)
        tree_scroll.pack(side="right", fill="y")
        
        ttk.Button(vlan_frame, text="🗑️ Eliminar Seleccionada", 
                  command=self.remove_vlan).pack(pady=5)
        
        # Botones de Acción
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(pady=10)
        
        ttk.Button(action_frame, text="🔍 Probar Conexión", 
                  command=self.test_connection).pack(side="left", padx=5)
        ttk.Button(action_frame, text="🚀 Ejecutar Automatización", 
                  command=self.execute_automation).pack(side="left", padx=5)
        ttk.Button(action_frame, text="📋 Generar Script", 
                  command=self.generate_script).pack(side="left", padx=5)
        ttk.Button(action_frame, text="🎭 Modo Demo", 
                  command=self.demo_mode).pack(side="left", padx=5)
        
        # Log de Salida
        log_frame = ttk.LabelFrame(main_frame, text="Log de Ejecución", padding="10")
        log_frame.pack(fill="both", expand=True, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, width=80, 
                                                  font=('Courier', 9))
        self.log_text.pack(fill="both", expand=True)
        
        ttk.Button(log_frame, text="🧹 Limpiar Log", 
                  command=self.clear_log).pack(pady=5)
        
    def enable_mousewheel(self, canvas):
        """Habilitar scroll con rueda del mouse"""
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
    def log(self, message):
        """Agregar mensaje al log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def clear_log(self):
        """Limpiar el log"""
        self.log_text.delete(1.0, tk.END)
        
    def add_vlan(self):
        """Agregar VLAN a la lista"""
        try:
            vlan_id = int(self.vlan_id_entry.get())
            vlan_name = self.vlan_name_entry.get().strip()
            subnet = self.subnet_entry.get().strip()
            
            if not vlan_name:
                messagebox.showerror("Error", "El nombre de VLAN no puede estar vacío")
                return
                
            if vlan_id < 1 or vlan_id > 4094:
                messagebox.showerror("Error", "VLAN ID debe estar entre 1 y 4094")
                return
            
            # Validar subred
            network = ipaddress.ip_network(subnet, strict=False)
            gateway = str(list(network.hosts())[0])
            
            # Verificar si ya existe
            for item in self.vlan_tree.get_children():
                if self.vlan_tree.item(item)['values'][0] == vlan_id:
                    messagebox.showerror("Error", f"VLAN {vlan_id} ya existe")
                    return
            
            self.vlan_tree.insert("", tk.END, values=(vlan_id, vlan_name, subnet, gateway))
            
            # Limpiar campos
            self.vlan_id_entry.delete(0, tk.END)
            self.vlan_name_entry.delete(0, tk.END)
            self.subnet_entry.delete(0, tk.END)
            self.subnet_entry.insert(0, "192.168.1.0/24")
            
            self.log(f"✓ VLAN {vlan_id} ({vlan_name}) agregada")
            
        except ValueError as e:
            messagebox.showerror("Error", f"Error en los datos: {str(e)}")
            
    def remove_vlan(self):
        """Eliminar VLAN seleccionada"""
        selected = self.vlan_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione una VLAN para eliminar")
            return
            
        for item in selected:
            vlan_id = self.vlan_tree.item(item)['values'][0]
            self.vlan_tree.delete(item)
            self.log(f"✗ VLAN {vlan_id} eliminada")
            
    def get_vlans(self):
        """Obtener lista de VLANs configuradas"""
        vlans = []
        for item in self.vlan_tree.get_children():
            values = self.vlan_tree.item(item)['values']
            vlans.append({
                'id': values[0],
                'name': values[1],
                'subnet': values[2],
                'gateway': values[3]
            })
        return vlans
        
    def test_connection(self):
        """Probar conexión al dispositivo"""
        host = self.host_entry.get()
        user = self.user_entry.get()
        password = self.pass_entry.get()
        protocol = self.protocol_var.get()
        port = int(self.port_entry.get())
        timeout = int(self.timeout_entry.get())
        
        self.log(f"🔍 Probando conexión {protocol} a {host}:{port}... (timeout: {timeout}s)")
        
        try:
            if protocol == "SSH":
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(host, port=port, username=user, password=password, timeout=timeout)
                client.close()
                self.log("✓ Conexión SSH exitosa")
                messagebox.showinfo("Éxito", "Conexión SSH establecida correctamente")
            else:
                tn = telnetlib.Telnet(host, port, timeout=timeout)
                time.sleep(1)
                output = tn.read_very_eager().decode('ascii', errors='ignore')
                
                if "Username:" in output or "login:" in output:
                    tn.write(user.encode('ascii') + b"\n")
                    time.sleep(1)
                    output = tn.read_very_eager().decode('ascii', errors='ignore')
                
                if "Password:" in output or "password:" in output:
                    tn.write(password.encode('ascii') + b"\n")
                    time.sleep(1)
                
                tn.close()
                self.log("✓ Conexión Telnet exitosa")
                messagebox.showinfo("Éxito", "Conexión Telnet establecida correctamente")
                
        except Exception as e:
            self.log(f"✗ Error de conexión: {str(e)}")
            messagebox.showerror("Error", f"No se pudo conectar al dispositivo:\n{str(e)}\n\nVerifica:\n- IP correcta del router\n- Router en la misma red que tu PC\n- Telnet habilitado en el router")
            
    def execute_automation(self):
        """Ejecutar automatización de VLANs"""
        vlans = self.get_vlans()
        
        if not vlans:
            messagebox.showwarning("Advertencia", "No hay VLANs configuradas")
            return
            
        host = self.host_entry.get()
        user = self.user_entry.get()
        password = self.pass_entry.get()
        protocol = self.protocol_var.get()
        port = int(self.port_entry.get())
        
        self.log("=" * 60)
        self.log(f"🚀 Iniciando automatización en {host}")
        self.log(f"📊 VLANs a configurar: {len(vlans)}")
        self.log("=" * 60)
        
        try:
            if protocol == "SSH":
                self.execute_ssh(host, port, user, password, vlans)
            else:
                self.execute_telnet(host, port, user, password, vlans)
                
            self.log("=" * 60)
            self.log("✓ Automatización completada exitosamente")
            self.log("=" * 60)
            messagebox.showinfo("Éxito", "Automatización completada correctamente")
            
        except Exception as e:
            self.log(f"✗ Error durante la automatización: {str(e)}")
            messagebox.showerror("Error", f"Error durante la automatización:\n{str(e)}")
            
    def execute_ssh(self, host, port, user, password, vlans):
        """Ejecutar configuración via SSH"""
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        self.log("Conectando via SSH...")
        client.connect(host, port=port, username=user, password=password, timeout=10)
        
        shell = client.invoke_shell()
        time.sleep(1)
        shell.recv(1000)
        
        commands = self.generate_cisco_commands(vlans)
        
        for cmd in commands:
            self.log(f"  > {cmd}")
            shell.send(cmd + "\n")
            time.sleep(0.5)
            output = shell.recv(1000).decode('utf-8', errors='ignore')
            
        client.close()
        
    def execute_telnet(self, host, port, user, password, vlans):
        """Ejecutar configuración via Telnet"""
        self.log("Conectando via Telnet...")
        tn = telnetlib.Telnet(host, port, timeout=10)
        
        time.sleep(1)
        # Leer buffer inicial
        tn.read_very_eager()
        
        # Login
        tn.write(user.encode('ascii') + b"\n")
        time.sleep(1)
        tn.read_very_eager()
        
        tn.write(password.encode('ascii') + b"\n")
        time.sleep(2)
        tn.read_very_eager()
        
        commands = self.generate_cisco_commands(vlans)
        
        for cmd in commands:
            self.log(f"  > {cmd}")
            tn.write(cmd.encode('ascii') + b"\r\n")
            time.sleep(0.8)
            
            # Leer respuesta
            output = tn.read_very_eager().decode('ascii', errors='ignore')
            
            # Detectar errores
            if "Invalid" in output or "%" in output:
                self.log(f"    ⚠️ Advertencia: {output.strip()}")
            
        time.sleep(1)
        tn.close()
        
    def generate_cisco_commands(self, vlans):
        """Generar comandos para Cisco IOS"""
        commands = [
            "enable",
            "configure terminal"
        ]
        
        # Detectar si queremos comandos para router o switch
        # Por defecto usamos subinterfaces (routers)
        use_subinterfaces = True
        
        if use_subinterfaces:
            # Comandos para ROUTERS (subinterfaces)
            for vlan in vlans:
                clean_name = ''.join(c for c in vlan['name'] if c.isalnum() or c == ' ')
                
                commands.extend([
                    f"interface FastEthernet1/0.{vlan['id']}",
                    f"description {clean_name}",
                    f"encapsulation dot1Q {vlan['id']}",
                    f"ip address {vlan['gateway']} {self.get_netmask(vlan['subnet'])}",
                    "no shutdown",
                    "exit"
                ])
            
            # Activar interfaz principal
            commands.extend([
                "interface FastEthernet1/0",
                "no shutdown",
                "exit"
            ])
        else:
            # Comandos para SWITCHES (VLANs + SVI)
            for vlan in vlans:
                clean_name = ''.join(c for c in vlan['name'] if c.isalnum() or c == ' ')
                
                commands.extend([
                    f"vlan {vlan['id']}",
                    f"name {clean_name}",
                    "exit"
                ])
            
            for vlan in vlans:
                commands.extend([
                    f"interface vlan {vlan['id']}",
                    f"ip address {vlan['gateway']} {self.get_netmask(vlan['subnet'])}",
                    "no shutdown",
                    "exit"
                ])
        
        commands.extend([
            "end",
            "write memory",
            "exit"
        ])
        
        return commands
        
    def get_netmask(self, subnet):
        """Obtener máscara de subred desde notación CIDR"""
        network = ipaddress.ip_network(subnet, strict=False)
        return str(network.netmask)
        
    def demo_mode(self):
        """Modo demostración sin conexión real"""
        vlans = self.get_vlans()
        
        if not vlans:
            messagebox.showwarning("Advertencia", "No hay VLANs configuradas")
            return
            
        self.log("=" * 60)
        self.log("🎭 MODO DEMOSTRACIÓN ACTIVADO")
        self.log("=" * 60)
        self.log(f"📊 Simulando configuración de {len(vlans)} VLANs...")
        self.log("")
        
        commands = self.generate_cisco_commands(vlans)
        
        for i, cmd in enumerate(commands):
            self.log(f"  > {cmd}")
            self.root.update_idletasks()
            time.sleep(0.3)
            
        self.log("")
        self.log("✓ Comandos ejecutados exitosamente (SIMULACIÓN)")
        self.log("=" * 60)
        self.log("📝 Verificación simulada:")
        
        for vlan in vlans:
            self.log(f"  ✓ VLAN {vlan['id']} ({vlan['name']}) - {vlan['subnet']}")
            
        self.log("=" * 60)
        messagebox.showinfo("Demo Completada", 
                          f"Demostración completada.\n\n"
                          f"VLANs simuladas: {len(vlans)}\n"
                          f"Comandos ejecutados: {len(commands)}\n\n"
                          f"Este modo es ideal para presentaciones.")
        
    def generate_script(self):
        """Generar script de configuración"""
        vlans = self.get_vlans()
        
        if not vlans:
            messagebox.showwarning("Advertencia", "No hay VLANs configuradas")
            return
            
        commands = self.generate_cisco_commands(vlans)
        script = "\n".join(commands)
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            with open(filename, 'w') as f:
                f.write(f"! Script generado: {datetime.now()}\n")
                f.write(f"! VLANs configuradas: {len(vlans)}\n!\n")
                f.write(script)
            
            self.log(f"📋 Script guardado en: {filename}")
            messagebox.showinfo("Éxito", f"Script guardado en:\n{filename}")
            
    def save_configuration(self):
        """Guardar configuración actual"""
        vlans = self.get_vlans()
        
        if not vlans:
            messagebox.showwarning("Advertencia", "No hay VLANs para guardar")
            return
            
        name = simpledialog.askstring("Guardar Configuración", 
                                         "Nombre de la configuración:")
        
        if name:
            config = {
                'name': name,
                'timestamp': datetime.now().isoformat(),
                'vlans': vlans,
                'connection': {
                    'host': self.host_entry.get(),
                    'user': self.user_entry.get(),
                    'protocol': self.protocol_var.get(),
                    'port': self.port_entry.get()
                }
            }
            
            found = False
            for i, cfg in enumerate(self.configurations):
                if cfg['name'] == name:
                    self.configurations[i] = config
                    found = True
                    break
                    
            if not found:
                self.configurations.append(config)
                
            self.save_configurations()
            self.update_config_list()
            self.log(f"💾 Configuración '{name}' guardada")
            messagebox.showinfo("Éxito", f"Configuración '{name}' guardada correctamente")
            
    def load_selected_config(self, event=None):
        """Cargar configuración seleccionada"""
        selection = self.config_combo.get()
        
        if not selection:
            return
            
        for config in self.configurations:
            if config['name'] == selection:
                for item in self.vlan_tree.get_children():
                    self.vlan_tree.delete(item)
                    
                for vlan in config['vlans']:
                    self.vlan_tree.insert("", tk.END, 
                                        values=(vlan['id'], vlan['name'], 
                                               vlan['subnet'], vlan['gateway']))
                
                conn = config['connection']
                self.host_entry.delete(0, tk.END)
                self.host_entry.insert(0, conn['host'])
                self.user_entry.delete(0, tk.END)
                self.user_entry.insert(0, conn['user'])
                self.protocol_var.set(conn['protocol'])
                self.port_entry.delete(0, tk.END)
                self.port_entry.insert(0, conn['port'])
                
                self.log(f"📂 Configuración '{selection}' cargada")
                break
                
    def new_configuration(self):
        """Crear nueva configuración"""
        for item in self.vlan_tree.get_children():
            self.vlan_tree.delete(item)
            
        self.config_combo.set("")
        self.log("📄 Nueva configuración iniciada")
        
    def delete_configuration(self):
        """Eliminar configuración seleccionada"""
        selection = self.config_combo.get()
        
        if not selection:
            messagebox.showwarning("Advertencia", "Seleccione una configuración")
            return
            
        if messagebox.askyesno("Confirmar", f"¿Eliminar '{selection}'?"):
            self.configurations = [c for c in self.configurations if c['name'] != selection]
            self.save_configurations()
            self.update_config_list()
            self.config_combo.set("")
            self.log(f"🗑️ Configuración '{selection}' eliminada")
            
    def export_configuration(self):
        """Exportar configuración a archivo JSON"""
        selection = self.config_combo.get()
        
        if not selection:
            messagebox.showwarning("Advertencia", "Seleccione una configuración")
            return
            
        for config in self.configurations:
            if config['name'] == selection:
                filename = filedialog.asksaveasfilename(
                    defaultextension=".json",
                    filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
                )
                
                if filename:
                    with open(filename, 'w') as f:
                        json.dump(config, f, indent=4)
                    self.log(f"📤 Configuración exportada a: {filename}")
                    messagebox.showinfo("Éxito", "Configuración exportada")
                break
                
    def update_config_list(self):
        """Actualizar lista de configuraciones"""
        names = [c['name'] for c in self.configurations]
        self.config_combo['values'] = names
        
    def load_configurations(self):
        """Cargar configuraciones desde archivo"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    self.configurations = json.load(f)
            except:
                self.configurations = []
        else:
            self.configurations = []
            
    def save_configurations(self):
        """Guardar configuraciones a archivo"""
        with open(self.config_file, 'w') as f:
            json.dump(self.configurations, f, indent=4)


def main():
    root = tk.Tk()
    app = VLANAutomator(root)
    root.mainloop()


if __name__ == "__main__":
    main()