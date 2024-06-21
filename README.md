# PI1-KATIAU-BACK-END

Back-end para o carrinho seguidor de linha KATIAU. Utiliza o FastApi e SQLITE3.

## Instruções de como Rodar

Primeiramente tenha o `python 3.12.4` e crie um virtual env e associe esse virtual env ao seu terminal. Voce pode fazer isso exetuando estes comandos em seu terminal.

```bash
python -m venv .venv
source .venv/bin/activate
```

> **Importante**. Sempre rode o comando `source .venv/bin/activate` antes de iniciar o desenvolvimento
>
> Se estiver em um ambiente **Windows** você deve rodar o seguinte comando para ativar o virtual env.
>
> ```powershell
> .\.venv\Scripts\activate
> ```

Após isso você deve instalar os pacotes do ambiente descritos no `requirements.txt`. Para isso rode o seguinte comando

```bash
pip install -r requirements.txt
```

Crie um arquivo `.env` na raiz do projeto contendo essas informações
```
# .env
ENVIRONMENT=production #production
```
Por fim você pode executar a api em modo de desenvolvimento com o `fastapi dev`. Ele irá executar uma instância da API na url http://localhost:8000/. Para visualizar a documentação da API acesse http://localhost:8000/docs.

```bash
fastapi dev src/main.py
```

Para rodar a API em modo de produção execute

```bash
fastapi run src/main.py
```

# Testes
Para rodar os testes é necessário que tenha criado um arquivo `.env` na raíz do projeto. o `.env` deve conter as seguintes informações.

```
# .env
ENVIRONMENT=test #production
```

Após criar o `.env` rode o seguinte comando em seu terminal.

```
pytest
```