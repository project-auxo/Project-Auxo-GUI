# Place this local Flask app on the BBB
Flask app provides the REST endpoints through which the KIVY GUI interfaces. 


# Sending POST requests via curl 
One can use `curl -d 'status=0' http://192.168.0.101:5000/change_led_status`