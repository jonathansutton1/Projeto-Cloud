# Projeto Cloud
Projeto final da disciplina de Cloud - Insper 2023.1

## Objetivo do projeto
Desenvolver um código em terraform que consiga fazer a autenticação de usuários para entrar em uma aplicação web. Essa autenticação deve ser feita de maneira prática e segura.

## Estrutura do projeto
O projeto está organizado da seguinte forma:

**Pasta "terraform"**: Esta pasta contém o arquivo ```main.tf``` e o arquivo ```lambda_function_payload.zip```. O arquivo main.tf é responsável por instanciar os recursos necessários na AWS (descrição abaixo). O arquivo zip contém o código python que a função lambda vai executar.

**Pasta "lambda":** Essa pasta contém o arquivo ```lambda_function.py```, que será zipado após a instância ser feita, e irá substituir o zip da pasta "terraform" (mais detalhes na hora de executar o projeto). Esse arquivo será preenchido com o ID do userpool criado pelo cognito e o email cadastrado, e sua função é enviar um email com o login e senha do usuário.

**Arquivo ```app.py```:** Este arquivo contém a aplicação web que roda localmente, desenvolvida em Flask. Ele possui uma página para enviar o email com o usuário e outra página para fazer o login para entrar na aplicação.

## Recursos utilizados da AWS
- **AWS IAM:** O AWS Identity and Access Management (IAM) é um serviço que permite gerenciar o acesso seguro aos recursos da AWS. Ele controla as permissões e políticas de segurança, permitindo que você defina e gerencie as identidades que podem acessar seus recursos.

- **AWS Cognito:** O Amazon Cognito é um serviço que permite adicionar recursos de autenticação, autorização e gerenciamento de usuários em uma aplicação. Fornece um fluxo de registro e login seguro, que nesse projeto é enviado via email.

- **AWS API Gateway:** O Amazon API Gateway é um serviço totalmente gerenciado que permite criar, publicar, proteger e gerenciar APIs para seus aplicativos. Ele atua como um ponto de entrada para suas APIs, oferecendo recursos como autenticação, controle de acesso, monitoramento e transformação de dados.

- **AWS Lambda:** O AWS Lambda é um serviço de computação serverless que permite executar código sem precisar provisionar ou gerenciar servidores. Ele executa o código em resposta a eventos, como chamadas de API, uploads de arquivos ou alterações em um banco de dados. O AWS Lambda escala automaticamente a capacidade de acordo com a demanda e você paga apenas pelo tempo de execução real do código.

### Como o Lambda foi utilizado nesse projeto
O arquivo ```.py``` dentro da pasta zipada é um script que envia emails com o usuário e senha da pessoa que fazer a requisição a partir da aplicação web, e o lambda executa esse arquivo serverless.

## Topologia do projeto 
![image](https://github.com/jonathansutton1/Projeto-Cloud/assets/62657975/f218dec1-af09-41b0-b7c8-2508c460aebd)

## Pré-requisitos para rodar o projeto
- Ter o [Terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli) instalado na máquina.
- Ter o [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) instalado e configurado na máquina.
- Ter o [Python](https://www.python.org/) instalado na máquina

## Roteiro de instalação e funcionamento do projeto

- Clonar o repositório com o comando:
```git clone https://github.com/jonathansutton1/Projeto-Cloud/```

- A primeira coisa a se fazer é ir no painel do [SES](https://us-east-1.console.aws.amazon.com/ses/home?region=us-east-1#/account) e cadastrar o seu email como "email verificado". Após fazer isso lá, confirme no seu email a verificação de identidade.
- Depois é preciso criar um bucket via CLI, a partir do comando:

```aws s3api create-bucket --bucket nome_do_bucket --region us-east-1```
- Em "nome_do_bucket", trocar para o nome que você deseja por no bucket. Não se esqueça de mudar o nome também no arquivo ```main.tf``` (linha 7).


- No Command Prompt, dar os 3 comandos em seguida para subir o projeto na AWS:

 ```terraform init```
 
 ```terraform plan```
 
 ```terraform apply```
 
- Com isso, acesse o dashboard da AWS na página do [Cognito](https://us-east-1.console.aws.amazon.com/cognito/v2/idp/user-pools?region=us-east-1) e pegue o ID do user pool.
- Copie esse ID no arquivo ```lambda_function.py```
- Copie também o seu email que você cadastrou no SES.
- Crie um arquivo chamado ```lambda_function_payload.zip``` contendo esse arquivo Python e substitua ele pelo zip existente dentro da pasta 'terraform'
- Dê mais uma vez um  ```terraform plan``` e ```terraform apply```
- Depois disso, você terá 2 maneiras de criar seu usuário para entrar na aplicação:

### Opção 1
- A partir do comando abaixo é possível criar um usuário:

 ```aws cognito-idp admin-create-user --region us-east-1 --user-pool-id us-east-1_seuID --username usuario123 --user-attributes Name=email,Value=seu@email.com Name=email_verified,Value=true```
 
 Perceba que em "Value" é preciso por o seu email, pois a senha será enviada lá! Em "username" você poderá por o que quiser, e em "user-pool-id" substitua pelo seu ID do userpool (ver no cognito)
 
 - Com isso, acessar o seu email, onde será enviado seu usuário de login e senha.
 
 ***OBS***: No email, a frase vem "Your username is xxx and temporary password is yyy."
 
 O "." NÃO faz parte da senha!

- Para acessar a aplicação, basta ir na pasta principal do projeto e dar o comando  ```python app.py```
- A aplicação irá logar localmente no servidor local (http://127.0.0.1:5000)
- Acesse a página: http://127.0.0.1:5000/login (sim, precisa ter o /login)
- Para finalizar, use os valores enviados no email para logar. Caso dê certo, você será redirecionado para uma página que diz que você conseguiu entrar. Caso o usuário ou a senha estejma errados, volte para a página e logue de novo com o usuário ou a senha certa.

### Opção 2 
- Na página principal do projeto, dê o comando ```python app.py```.
- A aplicação irá logar localmente no servidor local (http://127.0.0.1:5000)
- Insira o seu email no campo de escrever, e clique em "Inscrever".

 ***OBS***: O email escrito deve estar cadastrado no [SES](https://us-east-1.console.aws.amazon.com/ses/home?region=us-east-1#/account).
 
- Verifique seu email. Você receberá seu usuário e senha por lá.
- Acesse a página: http://127.0.0.1:5000/login
- Utilize o usuário e senha enviados no email para entrar na aplicação.






