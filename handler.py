import sys
sys.path.insert(0,'/opt')

import json
import boto3
import os

from sqsHandler import SqsHandler
from env import Variables

def inseresqs(event, context):
    env = Variables()
    sqs = SqsHandler(env.get_sqs_url())
    sqsDest = SqsHandler(env.get_sqs_url_dest())
    
    mensagem = event['pathParameters']['mensagem']
    
    sqs.send(str(mensagem))
    
    body = {
         "Messagem " : str(mensagem)
    }
    
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

def recebe_sqs_principal_imprimir(event, context):
    env = Variables()
    sqs = SqsHandler(env.get_sqs_url())
    sqsDest = SqsHandler(env.get_sqs_url_dest())
    
    msgs = sqs.getMessage(10)
    
    texto = str(msgs)
    
    resposta = ""

    if texto[2:18] == "ResponseMetadata":
        resposta = "Nao ha mensagens"
    else:
        for msg in msgs['Messages']:
            resposta = resposta + str(msg['Body']) + ", "
            sqsDest.send(str(msg['Body']))
            sqs.deleteMessage(msg['ReceiptHandle'])

    body = {
         "Resposta " : str(resposta)
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }
    
    return response
    
def publica_topico(event, context):
    env =  Variables()
    sqsDest = SqsHandler(env.get_sqs_url_dest())
    
    msgs = sqsDest.getMessage(10)
    
    texto = str(msgs)
    
    resposta = ""
    
    if texto[2:18] == "ResponseMetadata":
        resposta = "Nao ha mensagens"
    else:
        for msg in msgs['Messages']:
            resposta = resposta + str(msg['Body'])  + ", "
    
    if texto[2:18] != "ResponseMetadata":        
        publish_message_to_sns(resposta)
    
    body = {
         "Mensagens enviadas " : str(resposta)
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
    
# def publish_message_to_sns(topicArn: str ,message: str):
def publish_message_to_sns(message: str):
    sns = boto3.client('sns')

    env = Variables()
    topico = env.get_arn_id()

    response = sns.publish(
        TopicArn=topico,
        Message=str(message),    
    )