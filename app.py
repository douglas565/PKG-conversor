#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extrator de PKG PS4 - Extração Completa
Extrai TODOS os arquivos .pkg do PlayStation 4 mantendo a estrutura completa
"""

import os
import sys
import struct
import json
from pathlib import Path
from datetime import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import zlib

class PS4PKGExtractor:
    def __init__(self, root):
        self.root = root
        self.root.title("Extrator de PKG PS4 - Completo")
        self.root.geometry("1000x750")
        self.root.resizable(True, True)
        
        # Variáveis
        self.pkg_file = None
        self.output_dir = None
        self.extracting = False
        
        # Cores tema PS4
        self.bg_color = "#1a1d29"
        self.fg_color = "#ffffff"
        self.accent_color = "#0070cc"
        self.success_color = "#00aa00"
        self.error_color = "#cc0000"
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configura a interface gráfica"""
        
        # Configurar cores
        self.root.configure(bg=self.bg_color)
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background=self.bg_color)
        style.configure('TLabel', background=self.bg_color, foreground=self.fg_color)
        style.configure('TButton', background=self.accent_color, foreground=self.fg_color)
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky=(tk.W, tk.E))
        
        title_label = tk.Label(
            header_frame, 
            text="🎮 EXTRATOR COMPLETO DE PKG PS4",
            font=("Arial", 20, "bold"),
            bg=self.bg_color,
            fg=self.accent_color
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            header_frame,
            text="Extrai TODOS os arquivos e pastas do pacote PKG",
            font=("Arial", 10),
            bg=self.bg_color,
            fg="#8899aa"
        )
        subtitle_label.pack()
        
        # Frame de seleção de arquivo
        file_frame = ttk.LabelFrame(main_frame, text="Selecionar Arquivo PKG", padding="10")
        file_frame.grid(row=1, column=0, pady=(0, 10), sticky=(tk.W, tk.E))
        
        self.file_label = tk.Label(
            file_frame,
            text="Nenhum arquivo selecionado",
            bg=self.bg_color,
            fg=self.fg_color,
            anchor="w"
        )
        self.file_label.pack(fill=tk.X, pady=(0, 5))
        
        btn_select = tk.Button(
            file_frame,
            text="📁 Selecionar PKG",
            command=self.select_pkg_file,
            bg=self.accent_color,
            fg=self.fg_color,
            font=("Arial", 10, "bold"),
            cursor="hand2"
        )
        btn_select.pack(fill=tk.X)
        
        # Frame de filtro de formato
        format_frame = ttk.LabelFrame(main_frame, text="Filtro de Arquivos ELF", padding="10")
        format_frame.grid(row=2, column=0, pady=(0, 10), sticky=(tk.W, tk.E))
        
        self.format_var = tk.StringVar(value="*.*")
        
        formats = [
            ("*.* (TODOS OS ARQUIVOS - Recomendado)", "*.*"),
            ("*.bin *.elf *.oelf (Apenas ELF)", "*.bin *.elf *.oelf"),
            ("*.bin (Binary)", "*.bin"),
            ("*.elf (ELF)", "*.elf"),
            ("*.oelf (Object ELF)", "*.oelf")
        ]
        
        for text, value in formats:
            rb = tk.Radiobutton(
                format_frame,
                text=text,
                variable=self.format_var,
                value=value,
                bg=self.bg_color,
                fg=self.fg_color,
                selectcolor="#2a2d39",
                activebackground=self.bg_color,
                activeforeground=self.fg_color
            )
            rb.pack(anchor=tk.W)
        
        # Frame de diretório de saída
        output_frame = ttk.LabelFrame(main_frame, text="Diretório de Saída", padding="10")
        output_frame.grid(row=3, column=0, pady=(0, 10), sticky=(tk.W, tk.E))
        
        self.output_label = tk.Label(
            output_frame,
            text="Pasta atual do programa",
            bg=self.bg_color,
            fg=self.fg_color,
            anchor="w"
        )
        self.output_label.pack(fill=tk.X, pady=(0, 5))
        
        btn_output = tk.Button(
            output_frame,
            text="📂 Escolher Pasta",
            command=self.select_output_dir,
            bg=self.accent_color,
            fg=self.fg_color,
            font=("Arial", 10, "bold"),
            cursor="hand2"
        )
        btn_output.pack(fill=tk.X)
        
        # Frame de informações do PKG
        info_frame = ttk.LabelFrame(main_frame, text="Informações do PKG", padding="10")
        info_frame.grid(row=1, column=1, rowspan=3, padx=(10, 0), pady=(0, 10), sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.info_text = scrolledtext.ScrolledText(
            info_frame,
            width=40,
            height=15,
            bg="#2a2d39",
            fg=self.fg_color,
            font=("Courier", 9),
            state='disabled'
        )
        self.info_text.pack(fill=tk.BOTH, expand=True)
        
        # Botões de ação
        action_frame = ttk.Frame(main_frame)
        action_frame.grid(row=4, column=0, columnspan=2, pady=(0, 10), sticky=(tk.W, tk.E))
        
        self.btn_extract = tk.Button(
            action_frame,
            text="⚡ EXTRAIR TUDO DO PKG",
            command=self.extract_pkg,
            bg=self.success_color,
            fg=self.fg_color,
            font=("Arial", 12, "bold"),
            height=2,
            cursor="hand2"
        )
        self.btn_extract.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        btn_clear = tk.Button(
            action_frame,
            text="🗑️ Limpar",
            command=self.clear_all,
            bg=self.error_color,
            fg=self.fg_color,
            font=("Arial", 12, "bold"),
            height=2,
            cursor="hand2"
        )
        btn_clear.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Barra de progresso
        progress_frame = ttk.Frame(main_frame)
        progress_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.progress_label = tk.Label(
            progress_frame,
            text="Pronto para extrair",
            bg=self.bg_color,
            fg=self.fg_color,
            font=("Arial", 9)
        )
        self.progress_label.pack(anchor=tk.W)
        
        self.progress = ttk.Progressbar(progress_frame, mode='determinate')
        self.progress.pack(fill=tk.X, pady=(5, 0))
        
        # Log de atividades
        log_frame = ttk.LabelFrame(main_frame, text="Log de Atividades", padding="10")
        log_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=12,
            bg="#000000",
            fg="#00ff00",
            font=("Courier", 9),
            state='disabled'
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Configurar expansão de grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(6, weight=1)
        
        self.add_log("Sistema iniciado. Pronto para extrair PKG completo!", "info")
        
    def add_log(self, message, log_type="info"):
        """Adiciona mensagem ao log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        color_map = {
            "info": "#00aaff",
            "success": "#00ff00",
            "error": "#ff0000",
            "warning": "#ffaa00"
        }
        
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, f"[{timestamp}] ", "timestamp")
        self.log_text.insert(tk.END, f"{message}\n", log_type)
        
        self.log_text.tag_config("timestamp", foreground="#888888")
        self.log_text.tag_config(log_type, foreground=color_map.get(log_type, "#ffffff"))
        
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')
        self.root.update()
        
    def update_info(self, info_dict):
        """Atualiza painel de informações"""
        self.info_text.config(state='normal')
        self.info_text.delete(1.0, tk.END)
        
        for key, value in info_dict.items():
            self.info_text.insert(tk.END, f"{key}:\n", "key")
            self.info_text.insert(tk.END, f"  {value}\n\n", "value")
        
        self.info_text.tag_config("key", foreground="#00aaff", font=("Courier", 9, "bold"))
        self.info_text.tag_config("value", foreground="#ffffff")
        
        self.info_text.config(state='disabled')
        
    def select_pkg_file(self):
        """Seleciona arquivo PKG"""
        filename = filedialog.askopenfilename(
            title="Selecionar arquivo PKG",
            filetypes=[("PKG Files", "*.pkg"), ("All Files", "*.*")]
        )
        
        if filename:
            self.pkg_file = filename
            self.file_label.config(text=os.path.basename(filename))
            self.add_log(f"Arquivo selecionado: {os.path.basename(filename)}", "success")
            self.analyze_pkg(filename)
            
    def select_output_dir(self):
        """Seleciona diretório de saída"""
        directory = filedialog.askdirectory(title="Selecionar pasta de saída")
        
        if directory:
            self.output_dir = directory
            self.output_label.config(text=directory)
            self.add_log(f"Pasta de saída: {directory}", "success")
            
    def analyze_pkg(self, filename):
        """Analisa o arquivo PKG"""
        try:
            with open(filename, 'rb') as f:
                # Ler header do PKG
                header = f.read(0x1000)  # Ler 4KB do header
                
                if len(header) < 32:
                    self.add_log("Arquivo PKG inválido ou corrompido", "error")
                    return
                
                # Parse header
                magic = struct.unpack('>I', header[0:4])[0]
                pkg_type = struct.unpack('>I', header[4:8])[0]
                pkg_revision = struct.unpack('>I', header[8:12])[0]
                header_size = struct.unpack('>H', header[12:14])[0]
                item_count = struct.unpack('>H', header[14:16])[0]
                pkg_size = struct.unpack('>Q', header[16:24])[0]
                data_offset = struct.unpack('>Q', header[24:32])[0]
                data_size = struct.unpack('>Q', header[32:40])[0]
                
                file_size = os.path.getsize(filename)
                
                info = {
                    "Nome do Arquivo": os.path.basename(filename),
                    "Tamanho Total": f"{file_size / (1024*1024):.2f} MB",
                    "Magic": f"0x{magic:08X}",
                    "Tipo": "PS4 PKG" if magic == 0x7F434E54 else "PKG Desconhecido",
                    "Revisão": f"{pkg_revision}",
                    "Tamanho Header": f"{header_size} bytes",
                    "Itens no PKG": f"{item_count}",
                    "Offset de Dados": f"0x{data_offset:X}",
                    "Tamanho Dados": f"{data_size / (1024*1024):.2f} MB",
                    "Status": "✓ Válido" if magic == 0x7F434E54 else "✗ Inválido"
                }
                
                self.update_info(info)
                self.add_log(f"PKG analisado: {item_count} itens encontrados", "success")
                
        except Exception as e:
            self.add_log(f"Erro ao analisar PKG: {str(e)}", "error")
            
    def extract_pkg(self):
        """Extrai o arquivo PKG"""
        if not self.pkg_file:
            messagebox.showerror("Erro", "Selecione um arquivo PKG primeiro!")
            return
        
        if self.extracting:
            messagebox.showwarning("Aviso", "Uma extração já está em andamento!")
            return
        
        # Executar em thread separada
        thread = threading.Thread(target=self._extract_pkg_thread)
        thread.daemon = True
        thread.start()
        
    def _extract_pkg_thread(self):
        """Thread de extração completa"""
        self.extracting = True
        self.btn_extract.config(state='disabled')
        
        try:
            # Diretório de saída
            output_base = self.output_dir if self.output_dir else os.getcwd()
            pkg_name = os.path.splitext(os.path.basename(self.pkg_file))[0]
            extract_dir = os.path.join(output_base, f"{pkg_name}_extracted")
            
            os.makedirs(extract_dir, exist_ok=True)
            self.add_log(f"Iniciando extração completa...", "info")
            self.add_log(f"Destino: {extract_dir}", "info")
            
            file_size = os.path.getsize(self.pkg_file)
            self.add_log(f"Tamanho do PKG: {file_size/(1024*1024):.2f} MB", "info")
            
            with open(self.pkg_file, 'rb') as f:
                # Ler apenas o header (não o arquivo todo!)
                f.seek(0)
                header_data = f.read(0x1000)
                
                # Parse header PKG PS4
                magic = struct.unpack('>I', header_data[0:4])[0]
                
                if magic != 0x7F434E54:
                    raise Exception("PKG inválido: Magic number incorreto")
                
                # Ler informações do header
                table_offset = struct.unpack('>I', header_data[0x18:0x1C])[0]
                entry_count_header = struct.unpack('>I', header_data[0x10:0x14])[0]
                
                self.add_log(f"Offset da tabela (header): 0x{table_offset:X}", "info")
                self.add_log(f"Entradas no header: {entry_count_header}", "info")
                
                # Lista de offsets possíveis para tabelas de entrada
                possible_table_offsets = [
                    table_offset,
                    0x2A80,
                    0x3000,
                    0x4000,
                    0x1000,
                    0x2000
                ]
                
                all_entries = []
                formats = self.format_var.get().split()
                
                # Escanear cada offset possível (sem carregar arquivo inteiro)
                for base_offset in possible_table_offsets:
                    if base_offset >= file_size:
                        continue
                    
                    self.add_log(f"Escaneando tabela em 0x{base_offset:X}...", "info")
                    
                    # Ler apenas a região da tabela (não o arquivo inteiro!)
                    max_entries_to_scan = 500
                    table_size = max_entries_to_scan * 32
                    
                    f.seek(base_offset)
                    table_data = f.read(table_size)
                    
                    # Processar entradas da tabela
                    for idx in range(max_entries_to_scan):
                        entry_start = idx * 32
                        if entry_start + 32 > len(table_data):
                            break
                        
                        entry_bytes = table_data[entry_start:entry_start+32]
                        
                        try:
                            entry_id = struct.unpack('>I', entry_bytes[0:4])[0]
                            entry_offset = struct.unpack('>I', entry_bytes[16:20])[0]
                            entry_size = struct.unpack('>I', entry_bytes[20:24])[0]
                            
                            # Validações
                            if entry_size == 0 or entry_size > 2*1024*1024*1024:
                                continue
                            
                            if entry_offset == 0 or entry_offset >= file_size:
                                continue
                            
                            # Evitar duplicatas
                            if any(e['id'] == entry_id and e['offset'] == entry_offset for e in all_entries):
                                continue
                            
                            # Entrada válida
                            all_entries.append({
                                'id': entry_id,
                                'offset': entry_offset,
                                'size': entry_size
                            })
                            
                        except:
                            continue
                
                self.add_log(f"✓ {len(all_entries)} entradas únicas encontradas!", "success")
                
                if len(all_entries) == 0:
                    self.add_log("Nenhuma entrada válida encontrada!", "error")
                    raise Exception("Não foi possível localizar entradas no PKG")
                
                self.progress['maximum'] = len(all_entries)
                extracted_files = []
                
                # Extrair cada arquivo (streaming, sem carregar tudo na memória)
                for i, entry in enumerate(all_entries):
                    try:
                        entry_id = entry['id']
                        entry_offset = entry['offset']
                        entry_size = entry['size']
                        
                        # Mapeamento de IDs conhecidos
                        file_map = {
                            0x1: ("eboot.bin", ""),
                            0x1000: ("param.sfo", "sce_sys"),
                            0x1001: ("nptitle.dat", "sce_sys"),
                            0x1002: ("npbind.dat", "sce_sys"),
                            0x1003: ("selfinfo.dat", "sce_sys"),
                            0x1004: ("imageinfo.dat", "sce_sys"),
                            0x1005: ("target-deltainfo.dat", "sce_sys"),
                            0x1006: ("origin-deltainfo.dat", "sce_sys"),
                            0x1007: ("psreserved.dat", "sce_sys"),
                            0x1200: ("icon0.png", "sce_sys"),
                            0x1220: ("pic0.png", "sce_sys"),
                            0x1240: ("pic1.png", "sce_sys"),
                            0x1260: ("snd0.at9", "sce_sys"),
                            0x1280: ("changeinfo.xml", "sce_sys"),
                            0x1300: ("trophy_conf", "sce_sys"),
                            0x400: ("license.dat", "sce_sys"),
                            0x401: ("license.info", "sce_sys"),
                        }
                        
                        # Determinar nome do arquivo
                        if entry_id in file_map:
                            filename, subdir = file_map[entry_id]
                        elif entry_id >= 0x200 and entry_id < 0x260:
                            filename = f"module_{entry_id:04X}.prx"
                            subdir = "sce_module"
                        elif entry_id >= 0x1000 and entry_id < 0x1400:
                            filename = f"resource_{entry_id:04X}.dat"
                            subdir = "sce_sys"
                        elif entry_id >= 0x400 and entry_id < 0x500:
                            filename = f"playgo_{entry_id:04X}.dat"
                            subdir = "app"
                        else:
                            filename = f"file_{entry_id:04X}.bin"
                            subdir = "data"
                        
                        # Detectar tipo pelo conteúdo (ler apenas header)
                        f.seek(entry_offset)
                        header_sample = f.read(min(16, entry_size))
                        
                        if header_sample.startswith(b'\x7FELF'):
                            if '.bin' in filename or '.dat' in filename:
                                filename = filename.rsplit('.', 1)[0] + '.elf'
                        elif header_sample.startswith(b'\x00PSF'):
                            if '.sfo' not in filename and '.dat' in filename:
                                filename = filename.replace('.dat', '.sfo')
                        elif header_sample.startswith(b'\x89PNG'):
                            if '.png' not in filename:
                                filename = filename.rsplit('.', 1)[0] + '.png'
                        elif header_sample.startswith(b'<?xml'):
                            if '.xml' not in filename:
                                filename = filename.rsplit('.', 1)[0] + '.xml'
                        
                        # Verificar filtro
                        if not self._matches_filter(filename, formats):
                            self.progress['value'] = i + 1
                            continue
                        
                        # Criar diretórios
                        if subdir:
                            file_dir = os.path.join(extract_dir, subdir)
                            os.makedirs(file_dir, exist_ok=True)
                            file_path = os.path.join(file_dir, filename)
                            display_path = f"{subdir}/{filename}"
                        else:
                            file_path = os.path.join(extract_dir, filename)
                            display_path = filename
                        
                        # Extrair arquivo em chunks (para arquivos grandes)
                        f.seek(entry_offset)
                        
                        chunk_size = 8 * 1024 * 1024  # 8MB por vez
                        bytes_written = 0
                        
                        with open(file_path, 'wb') as out_file:
                            while bytes_written < entry_size:
                                chunk_to_read = min(chunk_size, entry_size - bytes_written)
                                chunk = f.read(chunk_to_read)
                                if not chunk:
                                    break
                                out_file.write(chunk)
                                bytes_written += len(chunk)
                        
                        extracted_files.append({
                            "name": filename,
                            "path": display_path,
                            "size": entry_size,
                            "id": entry_id,
                            "offset": entry_offset
                        })
                        
                        size_mb = entry_size / (1024*1024)
                        size_str = f"{size_mb:.2f} MB" if size_mb > 1 else f"{entry_size/1024:.1f} KB"
                        self.add_log(f"✓ [{i+1}/{len(all_entries)}] {display_path} ({size_str})", "success")
                        
                        self.progress['value'] = i + 1
                        self.progress_label.config(text=f"Extraindo: {i+1}/{len(all_entries)}")
                        self.root.update()
                        
                    except Exception as e:
                        self.add_log(f"Erro no item {i}: {str(e)}", "warning")
                        continue
                
                # Criar estrutura de diretórios adicional
                extra_dirs = ["sce_module", "app", "license"]
                for dir_name in extra_dirs:
                    dir_path = os.path.join(extract_dir, dir_name)
                    os.makedirs(dir_path, exist_ok=True)
                
                # Salvar informações da extração
                extraction_info = {
                    "pkg_file": os.path.basename(self.pkg_file),
                    "extraction_date": datetime.now().isoformat(),
                    "extract_directory": extract_dir,
                    "format_filter": self.format_var.get(),
                    "total_entries_found": len(all_entries),
                    "extracted_files": len(extracted_files),
                    "files": extracted_files
                }
                
                info_path = os.path.join(extract_dir, "extraction_info.json")
                with open(info_path, 'w', encoding='utf-8') as f:
                    json.dump(extraction_info, f, indent=2, ensure_ascii=False)
                
                self.progress_label.config(text="Extração concluída!")
                self.add_log(f"\n{'='*50}", "info")
                self.add_log(f"✅ EXTRAÇÃO COMPLETA CONCLUÍDA!", "success")
                self.add_log(f"📁 Local: {extract_dir}", "info")
                self.add_log(f"📊 Arquivos extraídos: {len(extracted_files)} de {len(all_entries)} encontrados", "info")
                self.add_log(f"{'='*50}", "info")
                
                messagebox.showinfo(
                    "Sucesso!",
                    f"PKG extraído completamente!\n\n"
                    f"Entradas encontradas: {len(all_entries)}\n"
                    f"Arquivos extraídos: {len(extracted_files)}\n"
                    f"Local: {extract_dir}\n\n"
                    f"Verifique o arquivo extraction_info.json para detalhes."
                )
                
        except Exception as e:
            self.add_log(f"❌ ERRO NA EXTRAÇÃO: {str(e)}", "error")
            messagebox.showerror("Erro", f"Erro ao extrair PKG:\n{str(e)}")
            
        finally:
            self.extracting = False
            self.btn_extract.config(state='normal')
            self.progress['value'] = 0
            self.progress_label.config(text="Pronto para extrair")
            
    def _matches_filter(self, filename, formats):
        """Verifica se arquivo corresponde ao filtro"""
        if "*.*" in formats:
            return True
        
        ext = os.path.splitext(filename)[1].lower()
        for fmt in formats:
            filter_ext = fmt.replace("*", "").lower()
            if filter_ext == ext:
                return True
        return False
    
    def _extract_by_signature(self, data, extract_dir, extracted_files, formats):
        """Extrai arquivos procurando por assinaturas conhecidas"""
        signatures = {
            b'\x7FELF': ('eboot.bin', ''),
            b'\x00PSF': ('param.sfo', 'sce_sys'),
            b'\x89PNG': ('icon0.png', 'sce_sys'),
            b'OggS': ('audio.ogg', 'sce_sys'),
        }
        
        for sig, (filename, subdir) in signatures.items():
            offset = data.find(sig)
            if offset != -1:
                # Tentar determinar o tamanho do arquivo
                # Para ELF, ler o tamanho do header
                if sig == b'\x7FELF' and offset + 64 <= len(data):
                    try:
                        # Ler tamanho do ELF do header
                        e_shoff = struct.unpack('<Q', data[offset+40:offset+48])[0]
                        if e_shoff > 0:
                            file_size = min(e_shoff + 0x10000, len(data) - offset)
                        else:
                            file_size = min(10*1024*1024, len(data) - offset)  # 10MB default
                    except:
                        file_size = min(10*1024*1024, len(data) - offset)
                elif sig == b'\x00PSF' and offset + 24 <= len(data):
                    try:
                        # PSF/SFO tem tamanho no header
                        file_size = struct.unpack('<I', data[offset+16:offset+20])[0]
                        file_size = min(file_size + 24, 100*1024, len(data) - offset)
                    except:
                        file_size = min(64*1024, len(data) - offset)
                elif sig == b'\x89PNG':
                    # Para PNG, procurar pelo final
                    end_marker = b'IEND\xae\x42\x60\x82'
                    end_offset = data.find(end_marker, offset)
                    if end_offset != -1:
                        file_size = end_offset - offset + 8
                    else:
                        file_size = min(2*1024*1024, len(data) - offset)
                else:
                    file_size = min(1024*1024, len(data) - offset)
                
                if not self._matches_filter(filename, formats):
                    continue
                
                # Extrair arquivo
                if subdir:
                    file_dir = os.path.join(extract_dir, subdir)
                    os.makedirs(file_dir, exist_ok=True)
                    file_path = os.path.join(file_dir, filename)
                    display_path = f"{subdir}/{filename}"
                else:
                    file_path = os.path.join(extract_dir, filename)
                    display_path = filename
                
                with open(file_path, 'wb') as f:
                    f.write(data[offset:offset+file_size])
                
                extracted_files.append({
                    "name": filename,
                    "path": display_path,
                    "size": file_size,
                    "offset": offset
                })
                
                self.add_log(f"✓ Extraído por assinatura: {display_path} ({file_size/1024:.1f} KB)", "success")
        
    def clear_all(self):
        """Limpa todos os campos"""
        self.pkg_file = None
        self.output_dir = None
        self.file_label.config(text="Nenhum arquivo selecionado")
        self.output_label.config(text="Pasta atual do programa")
        
        self.info_text.config(state='normal')
        self.info_text.delete(1.0, tk.END)
        self.info_text.config(state='disabled')
        
        self.log_text.config(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state='disabled')
        
        self.progress['value'] = 0
        self.progress_label.config(text="Pronto para extrair")
        
        self.add_log("Sistema limpo. Pronto para nova extração!", "info")

def main():
    root = tk.Tk()
    app = PS4PKGExtractor(root)
    root.mainloop()

if __name__ == "__main__":
    main()