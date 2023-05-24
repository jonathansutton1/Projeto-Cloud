import boto3
import os
import string
import random

def generate_temp_password(size=8, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def lambda_handler(event, context):
    ses = boto3.client('ses')
    cognito = boto3.client('cognito-idp', region_name='us-east-1')
    email = event['email']
    
    temp_password = generate_temp_password()
    
    try:
        response = cognito.admin_create_user(
            UserPoolId='',  # Escreva o ID do seu User Pool aqui
            Username=email,
            TemporaryPassword=temp_password,
            UserAttributes=[
                {
                    'Name': 'email',
                    'Value': email
                },
            ],
            MessageAction='SUPPRESS'  # Não enviar e-mails de convite.
        )
        
        ses.send_email(
            Source='',    #Escreva seu email aqui
            Destination={
                'ToAddresses': [
                    email,
                ],
            },
            Message={
                'Subject': {
                    'Data': 'Confirmação de Identidade',
                    'Charset': 'UTF-8'
                },
                'Body': {
                    'Text': {
                        'Data': 'Confirme sua identidade clicando no link abaixo. Seu usuário é: {} e sua senha temporária é: {}'.format(email, temp_password),
                        'Charset': 'UTF-8'
                    }
                }
            }
        )
        
        return {
            'statusCode': 200,
            'body': 'Email enviado'
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': 'Erro ao criar usuário'
        }
