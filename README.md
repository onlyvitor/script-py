# Instalador mottainAI para Windows

Script em Python que executa o comando `curl` solicitado, verifica o arquivo baixado e o move para a pasta **Downloads** do usuário.

> **Importante:** a URL `/blob/` do GitHub usada no comando padrão retorna uma página HTML, não o arquivo `install.sh`. O script detecta isso e informa a falha explicitamente. Para baixar o `install.sh` real, use a opção `--raw`.

## O que o script faz

1. Executa o comando `curl` em uma pasta temporária.
2. Mostra todo o `stdout`/`stderr` do curl e o código de saída.
3. Verifica tamanho, SHA-256, primeira linha e tipo do arquivo.
4. Move o arquivo para a pasta Downloads do usuário.
5. Exibe um resumo final informando se o programa foi instalado ou não.

O script **não executa** o `install.sh` e **não instala** Bun, Git ou dependências.

## Requisitos

- Windows 10 ou 11.
- Python 3.8 ou superior instalado.
- `curl` disponível no PATH. No Windows 10/11, normalmente já vem em `C:\Windows\System32\curl.exe`.

## Como executar

Abra o **PowerShell** na pasta do script e execute:

```powershell
python instalar_mottainai_windows.py
```

Esse comando usa exatamente a URL informada:

```text
https://github.com/onlyvitor/mottainAI/blob/main/install.sh
```

Como essa URL retorna HTML, o script move o arquivo para Downloads, mas finaliza com falha e mostra o motivo.

## Como baixar o instalador real

Use a opção `--raw`:

```powershell
python instalar_mottainai_windows.py --raw
```

Nesse modo, o script baixa o arquivo bruto:

```text
https://raw.githubusercontent.com/onlyvitor/mottainAI/main/install.sh
```

O arquivo será movido para Downloads com o nome `motainnai`.

> Mesmo com `--raw`, o script apenas baixa e move o arquivo. Ele **não executa** o `install.sh`. Esse script é feito para Bash (Linux/macOS) e, no Windows, exigiria WSL ou Git Bash, além de Bun e Git.

## Escolher outra pasta de destino

```powershell
python instalar_mottainai_windows.py --raw --downloads-dir "D:\Downloads"
```

Se a pasta não existir, o script tenta criá-la.

## Onde o arquivo fica

Por padrão, o arquivo é salvo em:

```text
C:\Users\<seu-usuario>\Downloads\motainnai
```

O script usa a pasta Downloads oficial do Windows, inclusive quando ela foi redirecionada para o OneDrive. Se já existir um arquivo com esse nome e conteúdo diferente, ele cria um backup antes de substituir. Se o conteúdo for idêntico, o arquivo existente é mantido.

## Códigos de saída

| Código | Significado |
|--------|-------------|
| `0` | `install.sh` válido baixado e movido para Downloads (não executado). |
| `1` | Falha operacional: curl ausente, erro de rede, falha ao mover etc. |
| `2` | O conteúdo baixado não é o instalador esperado, como uma página HTML. |

## Ajuda

Para ver todas as opções:

```powershell
python instalar_mottainai_windows.py --help
```

## Problemas comuns

### `curl` não encontrado

Verifique se o arquivo existe:

```text
C:\Windows\System32\curl.exe
```

Se não existir, instale o curl e adicione-o ao PATH.

### `python` não encontrado

Instale o Python pelo site oficial ou pela Microsoft Store e marque a opção para adicionar o Python ao PATH durante a instalação.

### O arquivo baixado é HTML

Isso acontece porque a URL padrão é uma página do GitHub (`/blob/`). Use `--raw` para baixar o `install.sh` real.
