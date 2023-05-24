# Projeto Cloud
Projeto final da disciplina de Cloud - Insper 2023.1


## Pré-requisitos para rodar o projeto
- Ter o [Terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli) instalado na máquina.
- Ter o [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) instalado e configurado na máquina.

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
- Depois disso, você poderá criar o seu usuário para entrar na aplicação a partir do comando abaixo:

 ```aws cognito-idp admin-create-user --region us-east-1 --user-pool-id us-east-1_seuID --username usuario123 --user-attributes Name=email,Value=seu@email.com Name=email_verified,Value=true```
 
 Perceba que em "Value" é preciso por o seu email, pois a senha será enviada lá! Em "username" você poderá por o que quiser, e em "user-pool-id" substitua pelo seu ID do userpool (ver no cognito)
 
 - Com isso, acessar o seu email, onde será enviado seu usuário de login e senha.
 
 ***OBS***: No email, a frase vem "Your username is xxx and temporary password is yyy."
 
 O "." NÃO faz parte da senha!

- Para acessar a aplicação, basta ir na pasta principal do projeto e dar o comando  ```python app.py```
- A aplicação irá logar localmente no servidor local (http://127.0.0.1:5000)
- Acesse a página: http://127.0.0.1:5000/login (sim, precisa ter o /login)
- Para finalizar, use os valores enviados no email para logar. Caso dê certo, você será redirecionado para uma página que diz que você conseguiu entrar. Caso o usuário ou a senha estejma errados, volte para a página e logue de novo com o usuário ou a senha certa.





