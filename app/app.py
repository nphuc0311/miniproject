from flask import Flask, render_template
from flask_mqtt import Mqtt
from bs4 import BeautifulSoup
app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = 'mqtt.flespi.io'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = 'WSVFxw7Lhodp2v6zSqYQiNHIAwvodbTXTEseYpN5ERjuafTStFyBg47HqtVruCeb'
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_REFRESH_TIME'] = 1.0 # refresh time in seconds
mqtt = Mqtt(app)
def modify_html_body(file_path, new_content):
    with open(file_path, 'r') as file:
        # Đọc nội dung của tệp HTML
        html_content = file.read()

    # Sử dụng BeautifulSoup để phân tích cú pháp HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Tìm phần tử <body>
    body = soup.body

    if body:
        # Thay đổi nội dung của phần tử <body> thành nội dung mới
        body.string = new_content

        # Ghi nội dung đã chỉnh sửa vào tệp HTML
        with open(file_path, 'w') as file:
            file.write(str(soup))

@app.route('/')
def index():
    return render_template('index.html')

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('home/mytopic')


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
    topic=message.topic,
    payload=message.payload.decode()
    )
    modify_html_body('app/templates/index.html', data['payload'])
    # print(data)

if __name__ == "__main__":
    app.run(debug=True)