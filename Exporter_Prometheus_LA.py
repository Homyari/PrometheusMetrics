import os
import asyncio
from time import ctime
from http.server import BaseHTTPRequestHandler, HTTPServer

#global variables
load_min = 0
new_ip_counter = 0
day = 0
address = 'len_new_ip.txt' #macos
#address = '/root/SevaMetrics/len_new_ip.txt' #linux

#test1, test2 = 0, 0

class MetricsHandler(BaseHTTPRequestHandler):
    def do_GET(self): #HTTP request handler 
        if self.path == "/metrics":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            response = f"prometheus_metric_load_average_1_min {load_min}\nprometheus_metric_new_ip_counter {new_ip_counter}\n" #metrics to http, #{test1} {test2} for time_conflict_tests
            self.wfile.write(response.encode())
        else:
            self.send_response(404)
            self.end_headers()

async def load_average(): #prometheus metric load average for 1 minute
    global load_min #test1 for time_conflict_test
    while True: 
        load_min = float(os.popen("uptime | awk '{print $10}'").read().strip().replace(',','.')) #macos #take column 10, which shows the average load for 1 minute
        #load_min = os.popen("uptime | awk '{print $10}'").read().strip()[:-1] #linux
        
        await asyncio.sleep(120)

        #test1 +=1 #time_conflict_test
        #await asyncio.sleep(3) #sleep_test

async def count_ip(): #prometheus metric new ip counter for day
    global new_ip_counter, day, address #test2 for time_conflict_test

    while True:
        if int(ctime().split()[2]) != day: #updating counter, variable "day" and rewrite file with counter every day
            new_ip_counter, day = 0, int(ctime().split()[2])
            with open(address, 'w') as file_len_ip_reset:
                file_len_ip_reset.write('0')

        ip_base = os.popen(r"last | sort -k 3 | awk '{print $3}' | uniq -c | grep -E '([0-9]{1,3}\.){3}[0-9]{1,3}.*' | sort -k1 | wc -l").read().strip() #take the list with ip and count the number of rows in it 
        with open(address, 'r') as file_len_ip_read: #take the past number of rows from the previous check for comparisom
            length_ip = file_len_ip_read.read().strip()
        with open(address, 'w') as file_len_ip_write: #comparison of past and current number of rows
            if int(length_ip) != int(ip_base):
                print(int(length_ip), int(ip_base))
                new_ip_counter = int(ip_base) - int(length_ip)
            elif int(length_ip) == int(ip_base): 
                file_len_ip_write.write('0')
        #test2 +=5 for time_conflict_test
        await asyncio.sleep(10)
async def run_server(): #creating HTTP-server and geting events
    server = HTTPServer(("localhost", 9999), MetricsHandler)
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, server.serve_forever)

async def main(): #runs functions async
    await asyncio.gather(
        load_average(),
        count_ip(),
        run_server()
    )

if __name__ == "__main__":
    asyncio.run(main())