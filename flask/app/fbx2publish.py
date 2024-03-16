import pika

def notifyFbx2Publish(id: str, type: str):
    print(f"!!!!!!!!!!! Publishing FBX {id} of type {type} !!!!!!!!!!!!")
    rabbitmq_host = 'rabbitmq'
    queue_name = 'fbx2publish'

    credentials = pika.PlainCredentials('user', 'password')  # Use your RabbitMQ username and password
    connection_parameters = pika.ConnectionParameters(
        host=rabbitmq_host,
        credentials=credentials
    )
    connection = pika.BlockingConnection(connection_parameters)

    channel = connection.channel()

    channel.queue_declare(queue=queue_name, durable=True)

    # Publish a message
    message = "Ready to publish FBX"
    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=message,
        properties=pika.BasicProperties(
            headers={
                'GUID': id,
                'Type': type
                },
            delivery_mode=2,  # Makes the message persistent
        )
    )

    print(f"published fbx {message}")

    connection.close()
