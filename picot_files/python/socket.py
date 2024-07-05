import network
import socket
import time

pico_led = machine.Pin('LED', machine.Pin.OUT)

ssid = 'YOUR NETWORK'
password = 'YOUR PASSWORD'

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        time.sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip

def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    print(connection)
    return connection

def webpage(state):
    #Template HTML
    html = f"""
<!DOCTYPE html>
<html>
<body>
<form action="./lighton">
<input type="submit" value="Light on" />
</form>
<form action="./lightoff">
<input type="submit" value="Light off" />
</form>
<p>LED is {state}</p>
</body>
</html>"""
    return str(html)

def serve(connection):
    #Start a web server
    state = 'OFF'
    pico_led.off()
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        print(request)
        html = webpage(state)
        client.send(html)       
        client.close()

try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    machine.reset()
