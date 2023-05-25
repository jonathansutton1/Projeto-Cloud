import boto3
import os
import string
import random

def generate_temp_password(size=8, chars=string.ascii_letters + string.digits + string.punctuation):
    return ''.join(random.choice(chars) for _ in range(size))

def lambda_handler(event, context):
    ses = boto3.client('ses')
    cognito = boto3.client('cognito-idp', region_name='us-east-1')
    email = event['email']
    
    temp_password = generate_temp_password()
    
    try:
        response = cognito.admin_create_user(
            UserPoolId='us-east-1_JR64gnkoD',  # Escreva o ID do seu User Pool aqui
            Username=email,
            TemporaryPassword=temp_password,
            UserAttributes=[
                {
                    'Name': 'email',
                    'Value': email
                },
            ],
            MessageAction='SUPPRESS'  
        )
        
        ses.send_email(
            Source='jonathansutton56@gmail.com',    #Escreva seu email verificado aqui
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
                        'Data': 'Seu usuário é: {} e sua senha temporária é: {}'.format(email, temp_password),
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
    
