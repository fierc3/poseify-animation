import pika

def errorQueue(id: str, type: str, errMsg: str):
    print("!!!!!!!!!!! Error during animation creation")
    rabbitmq_host = 'rabbitmq'
    queue_name = 'error'

    credentials = pika.PlainCredentials('user', 'password')  # Use your RabbitMQ username and password
    connection_parameters = pika.ConnectionParameters(
        host=rabbitmq_host,
        credentials=credentials
    )
    connection = pika.BlockingConnection(connection_parameters)

    channel = connection.channel()

    channel.queue_declare(queue=queue_name, durable=True)

    # Publish a message
    message = f"Error occured for {id}"
    message_properties = pika.BasicProperties(
    headers={
        'GUID': id,
        'Type': type,
        "Error": errMsg
        },
    delivery_mode=2,  # Makes the message persistent
    )
    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=message,
        properties=message_properties
    )
    connection.close()
