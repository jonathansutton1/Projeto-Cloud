# Projeto Cloud
Projeto final da disciplina de Cloud - Insper 2023.1


## Pré-requisitos para rodar o projeto
- Ter o [Terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli) instalado na máquina.
- Ter o [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) instalado e configurado na máquina.

## Roteiro de instalação e funcionamento do projeto

- Clonar o repositório com o comando:
```git clone https://github.com/jonathansutton1/Projeto-Cloud/```
- No Command Prompt, dar os 3 comandos em seguida para subir o projeto na AWS:

 ```terraform init```
 
 ```terraform plan```
 
 ```terraform apply```
- Depois disso, você poderá criar o seu usuário para entrar na aplicação a partir do comando abaixo:

 ```aws cognito-idp admin-create-user --region us-east-1 --user-pool-id us-east-1_iQH4EJFH2 --username usuario@usuario.com --user-attributes Name=email,Value=seu@email.com Name=email_verified,Value=true```
 
 Perceba que em "Value" é preciso por o seu email, pois a senha será enviada lá! em "username" precisa ser no formato de email, mas você poderá por o que quiser.
 
 - Com isso, acessar o seu email, onde será enviado seu usuário de login e senha.

- Para acessar a aplicação, basta ir na pasta principal do projeto e dar o comando  ```python app.py```
- A aplicação irá logar localmente no servidor xxxxx
- Acesse a página: xxxx/login (sim, precisa ter o /login)
- Para finalizar, use os valores enviados no email para logar. Caso dê certo, você será redirecionado para uma página que diz que você conseguiu entrar. Caso a senha esteja errada, volte para a página e logue de novo com a senha certa.





