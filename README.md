Nesse repositorio vemos um crud em python utilizando Flask, Sqlalchemy e banco de dados MySql.
Ainda preciso fazer:

    > Com que as fotos dos jogos apareçam junto a lista da page de index
    > Melhorar o HTML e CSS.
    > Aprimorar o Banco de Dados.
        > Adicioanr mais dados sobre o usuario.
        > Definir se o usuario pode fazer modificações no site.
        > Adicionar comentarios e descrição.
    > Adicionar o Flask_Email para recuperação de senha
    > Adicionar um função simples de teste de venda de produto.

No ultimo commit foi adicionado:

    > Mais dados seram requisitados para o usuario.
    > descrição adicionada.

Erro:
    
    > Após o ultimo commit, a aplicação não irá funcionar 
        por erro no Banco de dados, Foreign Key error.

Iniciando a aplicação sera necessario que utilize o seguintes comandos no CMD:

        - -m venv venv
        - venv\scripts\activate
        - pip install requirements.txt

Em seguida sera necessario executar o 'models/prepara_banco.py', assim criando sera criado as tabelas com alguns jogos por padrão, então inicie a Aplicação executando o 'App.py'.
A partir deste momento sera criado um localhost para o acesso pelo navegador, acessando a pagina caso você queria fazer qualquer alteração nos jogos ou até mesmo deleta-lo, sera necessario entrar na pagina de Cadastro, após o cadastro sera necessario se logar, a partir dai você tera acesso total a api por enquanto.