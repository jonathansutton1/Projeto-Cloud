from flask import Flask, render_template, request, redirect, url_for
import boto3, json

app = Flask(__name__)

# Get the Cognito Client ID from SSM Parameter Store
ssm = boto3.client('ssm')
parameter = ssm.get_parameter(Name='/app/parameters/cognito_client_id', WithDecryption=True)
CLIENT_ID = parameter['Parameter']['Value']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form.get('email')
        client = boto3.client('lambda', region_name='us-east-1')
        response = client.invoke(
            FunctionName='lambda_function_name',
            InvocationType='Event',
            Payload=json.dumps({'email': email})
        )
        return 'Um e-mail de confirmação foi enviado para {}.'.format(email)

    return '''
        <form method="POST">
            E-mail: <input type="text" name="email">
            <input type="submit" value="Inscrever">
        </form>
    '''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        client = boto3.client('cognito-idp', region_name='us-east-1')
        try:
            response = client.initiate_auth(
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': username,
                    'PASSWORD': password,
                },
                ClientId=CLIENT_ID
            )

            if response.get('ChallengeName'):
                # If the user needs a new password, they'll be redirected to a different screen
                if response.get('ChallengeName') == 'NEW_PASSWORD_REQUIRED':
                   return 'Você entrou no aplicativo!'
            else:
                return 'Você entrou no aplicativo!'
        except client.exceptions.NotAuthorizedException:
            return 'Usuário ou senha inválidos.'

    return '''
        <form method="POST">
            Username: <input type="text" name="username">
            Password: <input type="password" name="password">
            <input type="submit" value="Login">
        </form>
    '''


@app.route('/email_verification_success', methods=['GET'])
def email_verification_success():
    return 'Obrigado por verificar seu email! Agora você pode acessar todos os recursos do nosso site.'

@app.route('/email_verification_fail', methods=['GET'])
def email_verification_fail():
    return 'Infelizmente, houve um problema ao verificar seu email. Por favor tente novamente.'

if __name__ == '__main__':
    app.run(debug=True)