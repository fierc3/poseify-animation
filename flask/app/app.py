from flask import Flask
import pika
import threading
from pose2fbx import startPose2Fbx
from error import errorQueue

app = Flask(__name__)
rabbitmq_host = 'rabbitmq'
credentials = pika.PlainCredentials('user', 'password')

@app.route('/')
def healthy():
    return "healhty!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

def start_consuming_pose2fbx():
    print("Starting consuming for pose2fbx")
    queue_name = 'pose2fbx'

    connection_parameters = pika.ConnectionParameters(
        host=rabbitmq_host,
        credentials=credentials
    )
    connection = pika.BlockingConnection(connection_parameters)
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)

    def callback(ch, method, properties, body):
        try:
            startPose2Fbx(properties.headers.get('GUID'), properties.headers.get('Type')) 
        except Exception as e:
            print(f"Error: {e}")
            errorQueue(properties.headers.get('GUID', 'unknown id'), properties.headers.get('Type', 'unknown type'), str(e))


    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        auto_ack=True
    )

    channel.start_consuming()

# Start the consuming process in a background thread
thread = threading.Thread(target=start_consuming_pose2fbx)
thread.start()
