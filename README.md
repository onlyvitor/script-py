# Instalador MottainAI para Windows

Script em Python responsável por baixar o instalador do MottainAI para Windows (`install.cmd`), validar o conteúdo recebido e movê-lo para a pasta **Downloads** do usuário.

> **Importante:** o arquivo esperado é um script Windows Batch (`.cmd`), não um script Bash (`.sh`). O instalador é destinado ao Windows e não depende de WSL ou Git Bash para ser baixado.

## O que o script faz

1. Executa o `curl` em uma pasta temporária.
2. Exibe o `stdout`, `stderr` e o código de saída do processo.
3. Verifica o tamanho, SHA-256, primeira linha e conteúdo do arquivo.
4. Identifica respostas HTML recebidas por engano no lugar do arquivo `.cmd`.
5. Move o instalador validado para a pasta Downloads.
6. Cria um backup caso já exista um arquivo anterior com o mesmo nome e conteúdo diferente.
7. Exibe um resumo da operação.

**O script Python não executa o instalador `.cmd` automaticamente.** Baixar e validar o arquivo não significa que o MottainAI foi instalado.

## Requisitos

- Windows 10 ou Windows 11.
- Python 3.8 ou superior.
- `curl` disponível no PATH.

O Windows 10 e 11 normalmente já incluem o curl em `C:\Windows\System32\curl.exe`.

## Como executar

Abra o PowerShell na pasta onde está o script Python:

```powershell
python instalar_mottainai_windows.py
```

O programa utilizará a URL configurada para obter o arquivo `install.cmd`.

**Atenção:** URLs do GitHub contendo `/blob/` apontam para páginas de visualização. Para baixar o conteúdo real, é necessário utilizar uma URL `raw.githubusercontent.com`.

## Arquivo esperado

O instalador deve ser um arquivo Batch:

```text
install.cmd
```

Exemplo de URL para obter o arquivo diretamente:

```text
https://raw.githubusercontent.com/onlyvitor/mottainAI/main/install.cmd
```

A URL deve corresponder ao caminho real do arquivo no repositório.

## Escolher outra pasta de destino

É possível definir manualmente onde o instalador será salvo:

```powershell
python instalar_mottainai_windows.py --downloads-dir "D:\Downloads"
```

Caso a pasta não exista, o programa tentará criá-la.

## Onde o arquivo fica

Por padrão, o arquivo será salvo em:

```text
C:\Users\<seu-usuario>\Downloads\install.cmd
```

O script deve utilizar a pasta Downloads do usuário, respeitando possíveis redirecionamentos, como pastas sincronizadas pelo OneDrive.

Se já existir um arquivo com o mesmo nome:

- Se o conteúdo for idêntico, o arquivo existente será preservado.
- Se o conteúdo for diferente, será criado um backup antes da substituição.

## Códigos de saída

| Código | Significado |
|---|---|
| `0` | Arquivo `.cmd` validado e salvo em Downloads. |
| `1` | Falha operacional, como curl ausente, erro de rede ou falha ao mover o arquivo. |
| `2` | Conteúdo recebido inválido ou incompatível com o instalador esperado. |

## Ajuda

Para visualizar as opções disponíveis:

```powershell
python instalar_mottainai_windows.py --help
```

## Problemas comuns

### `curl` não encontrado

Verifique se o executável está disponível:

```text
C:\Windows\System32\curl.exe
```

Se necessário, instale o curl e adicione sua localização ao PATH.

### `python` não encontrado

Instale o Python e habilite a opção de adicionar o executável ao PATH durante a instalação.

### O arquivo baixado é HTML

Isso geralmente acontece quando uma URL `/blob/` do GitHub é utilizada no lugar da URL do arquivo bruto.

Verifique se a URL configurada aponta para:

```text
https://raw.githubusercontent.com/
```

### O arquivo não foi reconhecido como Batch

Verifique se o caminho da URL aponta para o `install.cmd` correto e se o conteúdo recebido corresponde realmente a um script Windows Batch.

---

**Observação:** este projeto realiza somente o download, a validação e o armazenamento do instalador. A execução do `install.cmd` e a instalação do MottainAI são etapas independentes.