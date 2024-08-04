DOCUMENTAÇÃO DA API TASKS

Início do projeto:
Para iniciar o projeto, primeiro fizemos algumas coisas, levando em consideração que você já tem conhecimento da aplicação Django, nós começamos criando um repositório no github com o nome projetoTask.

Logo após nós clonarmos nosso repositório, e abrimos ele no nosso computador, e fizemos alguns comandos para deixar pronto para prosseguir.

Criamos nosso ambiente virtual usando o comando

  python -m venv venv

Nesse caso eu fiz o nosso projeto dentro do ambiente virtual, eu entrei na pasta, e usei nosso próximo comando dentro da pasta.

  python-admin startproject project


Em algumas empresas ou casos as pessoas usam fora do ambiente virtual, mas isso pode ocasionar o caso de subir coisas que existem dentro do venv para o repositório GIT.

Logo após dar start no nosso projeto nós vamos criar o nosso app dentro do projeto que é o nosso app taks e dentro dele nós vamos fazer a construção da nossa API.

Vamos criar alguns arquivos dentro do nosso projeto, o primeiro deles vai ser o urls.py, e o serializers.py.

No caso do urls.py vamos criar as rotas que vamos usar no nosso projeto, e o serializers.py, vamos usar para usar a nossa listagem de usuários.


As dependências que foram instaladas nesse projeto foram:

pip install djangorestframework
pip install psycopg2
pip install djangorestframework-simplejwt









Para usar a conexão com o banco de dados, eu apenas baixei o aplicativo da Postgres, e criei um banco de dados lá dentro, e após o banco ser criado, eu fiz a conexão com ele no meu projeto na parte de settings, logo após ter baixado a dependência psycopg2.


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'projecttask',
        'USER': 'postgres',
        'PASSWORD': '124578',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


Para me auxiliar também no projeto eu baixei o programa INSOMINIA, para poder fazer os testes nas rotas e validá-las.

As rotas foram feitas na nossa view do nosso projeto taks, dentro dela fizemos os imports daquilo que era necessário como, do api_view, autenticação, models etc..

Antes de apresentá-las apresentaremos também o modelo que foi criado para gerar a tabela e também as colunas que nossa API vai popular.
class Task(models.Model):
    title = models.CharField(max_length=250, blank=True)
    description = models.CharField(max_length=250, blank=True)
    due_date = models.DateField(blank=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    status = models.BooleanField('Ativo?', default=True)



ROTA DE POST:

	Essa rota tem como objetivo fazer o cadastro de uma task no nosso banco, ela solicita um corpo JSON, com os campos title, description e due_date, lembrando que os dois primeiros campos devem ser do tipo string e o due_date uma data válida.Caso alguns desses casos não seja respeitado pelo usuário, o erro equivalente irá aparecer. 

A rota usada no insomnia foi da seguinte forma: http://127.0.0.1:8000/taks/addtask/

e o corpo JSON:
{
  "title": "Fazer rotas GET",
  "description": "Desejo fazer as rotasd de GET com filtro de pesquisa",
  "due_date": "2024-08-10"
}


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_task(request, format=None):
    result = []
    data = request.data
    try:
        title = data.get('title')
        description = data.get('description')
        due_date = data.get('due_date')


        if not isinstance(title, str) or not isinstance(description, str):
            return Response(
                {"detail": "Title and description must be strings."},
                status=status.HTTP_400_BAD_REQUEST
            )
       
        try:
            due_date = datetime.strptime(due_date, '%Y-%m-%d')
        except (ValueError, TypeError):
            return Response(
                {"detail": "Due date must be a valid date in the format YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST
            )
   
        if not title or not description or not due_date:
            return Response(
                {"detail": "All fields (title, description, due_date) are required."},
                status=status.HTTP_400_BAD_REQUEST
            )


        # Cria a nova task
        task = Task(
            title=title,
            description=description,
            due_date=due_date,
        )
        task.save()


        result = f"Task {task.title} has been successfully registered!"
        result = {
            "result": result,
            "id": task.pk,
            "title": task.title,
            "description": task.description,
            "due_date": task.due_date,
            "created_at": task.created_at,
            "updated_at": task.updated_at,
        }
        return Response(result)
    except Exception as e:
        re = {
            "detail": f"Erro: {str(e)}"
        }
        return Response(re, status=status.HTTP_400_BAD_REQUEST)


ROTA DE GET:
	
	A nossa rota GET tem uma diferença ela pode fazer a exibição dos dados tanto de forma total como ela pode exibir apenas 1 dado. isso depende a forma como é passado a URL da rota, caso seja passado asssim:

http://127.0.0.1:8000/taks/listtask/

A rota vai fazer a exibição de todos os dados, mas caso seja passado com o parâmetro ID

http://127.0.0.1:8000/taks/listtask/?id=1

Ela irá realizar a filtragem e vai trazer apenas o dado que foi solicitado, caso seja passado um ID que não existe ou algum outro parâmetro a rota irá dar erro.


ROTA DE PUT:

	A rota PUT ela funciona quase da mesma forma que a rota POST mas como uma ressalva, na rota POTS você não pode mandar campos vazios, você sempre tem que mandar algo, já na rota PUT ela vai atualizar apenas os campos que você enviou na requisição, os outros permanecerão com seus dados caso não sejam madandos.
A rota usada no INSOMNIA:

http://127.0.0.1:8000/taks/edittask/?id=3

Lembrando que nessa rota você deve passar o parâmetro de ID, pois sem esse parâmetro não será possível atualizar o registro que você deseja.

Corpo do JSON:
{
  "title": "Fazer rotas DELETE",
  "description": "Desejo fazer as rotas de DELETE",
  "due_date": "2024-10-20"
}


ROTA DE DELETE:
	
	A rota de DELETE é a mais simples dentre suas irmãs pois, nela você apenas passa a URL, com o ID do registro que você quer deletar, mas com um porém, ele não faz a deleção do registro do banco, ele apenas muda o campo status para false, assim você não perde aquele registro que pode ser importante lá na frente.

A rota usada no INSOMNIA:

http://127.0.0.1:8000/taks/deletetask/?id=2

Bem de forma geral e abrangente eu mostrei na teoria como as rotas funcionam, mas há um porém para que elas sejam usadas, autenticação de token.

Para tal propósito eu usei uma biblioteca do Django que usa JWT, e que me gera uma rota que posso usar para gerar um token de um usuário e usa-lo na parte de 

HEADER -> Authorization -> Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIyNzUxNzQzLCJpYXQiOjE3MjI3NTE0NDMsImp0aSI6IjY1Mjc5MzMyODhjNjRkZWU5YmRiZGNhYzkxZTVkN2YxIiwidXNlcl9pZCI6MX0.MLN4Ok0yOZ0I8Q8wL6FJ4VsDB3-orSO9JemOAsJdqa4

Essa rota é a rota que eu uso para gerar os token:


http://127.0.0.1:8000/taks/token/

O retorno dela é o token de um usuário que pode ser usado nas rotas como permissão.

Dessa forma espero ter apresentado um pouco da API e como foi feita ela, desse modo, desejo a você desenvolvedor que está lendo que aguardo sua resposta.Até a proxima e que Deus abençoe a todos.
