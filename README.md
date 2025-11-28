# 🎮 Extrator de PKG PS4

Extrator completo de arquivos PKG do PlayStation 4 com interface gráfica amigável.

## 📋 Descrição

Este software permite extrair **todos os arquivos** contidos em pacotes PKG do PS4, mantendo a estrutura de diretórios original do sistema. Ideal para backup, análise de conteúdo e desenvolvimento.

## ✨ Características

- ✅ Interface gráfica intuitiva (Tkinter)
- ✅ Extração completa de todos os arquivos do PKG
- ✅ Suporte a arquivos PKG grandes (10GB+)
- ✅ Detecção automática de tipos de arquivo (ELF, PNG, SFO, XML)
- ✅ Filtros personalizados por extensão
- ✅ Barra de progresso em tempo real
- ✅ Log detalhado de todas as operações
- ✅ Exportação de relatório JSON com informações da extração
- ✅ Otimizado para não consumir muita memória RAM

## Visual:
![preview](https://github.com/user-attachments/assets/8b203ba6-81d3-4217-b08e-d9846ba83bd2)


## 🎯 Arquivos Extraídos

### Estrutura de Diretórios PS4:
```
jogo_extracted/
├── eboot.bin                    # Executável principal do jogo
├── sce_sys/                     # Arquivos do sistema
│   ├── param.sfo               # Parâmetros do sistema
│   ├── icon0.png               # Ícone do jogo
│   ├── pic0.png / pic1.png     # Imagens de fundo
│   ├── nptitle.dat             # Dados NPTitle
│   └── ...
├── sce_module/                  # Bibliotecas e módulos
│   └── *.prx                   # Bibliotecas do sistema
├── app/                         # Dados da aplicação
│   └── playgo_*.dat            # Chunks PlayGo
├── data/                        # Dados do jogo
└── license/                     # Informações de licença
```

## 💻 Requisitos

### Sistema Operacional:
- Windows 7/8/10/11
- Linux (todas as distribuições)
- macOS 10.12+

### Software:
- Python 3.6 ou superior
- Tkinter (geralmente já incluído no Python)

### Espaço em Disco:
- Espaço livre igual ou maior que o tamanho do PKG a ser extraído

## 🚀 Instalação

### Método 1: Executar Script Python

1. **Instalar Python:**
   - Baixe em: https://www.python.org/downloads/
   - Durante instalação, marque "Add Python to PATH"

2. **Baixar o script:**
   - Salve o arquivo como `pkg_extractor.py`

3. **Executar:**
   ```bash
   python pkg_extractor.py
   ```

### Método 2: Criar Executável (.exe)

1. **Instalar PyInstaller:**
   ```bash
   pip install pyinstaller
   ```

2. **Criar executável:**
   ```bash
   pyinstaller --onefile --windowed --name="PS4_PKG_Extractor" --icon=icon.ico pkg_extractor.py
   ```

3. **Executar:**
   - O executável estará em `dist/PS4_PKG_Extractor.exe`
   - Basta clicar duas vezes para abrir

## 📖 Como Usar

### Passo a Passo:

1. **Abra o programa**
   - Execute o script Python ou o executável .exe

2. **Selecione o arquivo PKG**
   - Clique em "📁 Selecionar PKG"
   - Navegue até o arquivo .pkg do PS4
   - Aguarde a análise automática do arquivo

3. **Configure o filtro (opcional)**
   - Escolha quais tipos de arquivos extrair:
     - `*.*` - Todos os arquivos (recomendado)
     - `*.bin *.elf *.oelf` - Apenas executáveis
     - Filtros específicos por extensão

4. **Escolha a pasta de saída (opcional)**
   - Clique em "📂 Escolher Pasta"
   - Se não escolher, extrai na pasta do programa

5. **Extrair**
   - Clique em "⚡ EXTRAIR TUDO DO PKG"
   - Aguarde a conclusão (pode demorar dependendo do tamanho)
   - Verifique o log para acompanhar o progresso

6. **Resultado**
   - Os arquivos estarão em `[nome_do_pkg]_extracted/`
   - Um arquivo `extraction_info.json` terá detalhes da extração

## 📊 Informações Exibidas

Durante a análise, você verá:
- **Magic**: Identificador do formato PKG
- **Tipo**: PS4 PKG ou PKG Desconhecido
- **Tamanho Total**: Tamanho do arquivo PKG
- **Itens no PKG**: Número de entradas encontradas
- **Status**: Se o PKG é válido ou não

## 🔧 Filtros de Arquivos

### Tipos de Filtro:

| Filtro | Descrição |
|--------|-----------|
| `*.*` | Extrai TODOS os arquivos (recomendado) |
| `*.bin *.elf *.oelf` | Apenas executáveis ELF |
| `*.bin` | Apenas arquivos .bin |
| `*.elf` | Apenas arquivos .elf |
| `*.oelf` | Apenas arquivos .oelf |

## 📝 Arquivo extraction_info.json

Após a extração, é gerado um arquivo JSON com:
```json
{
  "pkg_file": "nome_do_jogo.pkg",
  "extraction_date": "2025-01-15T10:30:00",
  "extract_directory": "/caminho/completo",
  "format_filter": "*.*",
  "total_entries_found": 150,
  "extracted_files": 150,
  "files": [
    {
      "name": "eboot.bin",
      "path": "eboot.bin",
      "size": 15728640,
      "id": 1,
      "offset": 12288
    }
  ]
}
```

## ⚠️ Solução de Problemas

### Erro: "PKG inválido: Magic number incorreto"
- **Causa**: Arquivo não é um PKG válido ou está corrompido
- **Solução**: Verifique se o arquivo é realmente um PKG do PS4

### Erro: "Não foi possível localizar entradas no PKG"
- **Causa**: PKG com formato desconhecido ou criptografado
- **Solução**: Certifique-se que o PKG não está criptografado

### Programa travando ou fechando
- **Causa**: Arquivo muito grande consumindo memória
- **Solução**: Feche outros programas para liberar RAM

### Nenhum arquivo extraído
- **Causa**: Filtro muito restritivo
- **Solução**: Use o filtro `*.*` para extrair tudo

### Faltam arquivos na extração
- **Causa**: PKG com estrutura não padrão
- **Solução**: Verifique o log para ver quais arquivos falharam

## 🔒 Aviso Legal

Este software é fornecido apenas para fins educacionais e de backup pessoal. 

**IMPORTANTE:**
- ✅ Use apenas com PKGs que você possui legalmente
- ✅ Respeite os direitos autorais e termos de serviço
- ❌ Não use para pirataria ou distribuição ilegal
- ❌ O desenvolvedor não se responsabiliza pelo uso indevido

## 🐛 Reportar Problemas

Encontrou um bug? Tem uma sugestão?
- Descreva o problema detalhadamente
- Inclua o log de erro (se houver)
- Informe o sistema operacional e versão do Python

## 📜 Licença

Este projeto é distribuído sob licença MIT.

```
Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

## 👨‍💻 Autor

Desenvolvido com ❤️ para a comunidade PS4

---

## 🎮 Enjoy!

**Versão:** 1.0.0  
**Data:** Janeiro 2025  
**Compatibilidade:** PS4 PKG Format
