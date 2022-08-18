from serial.serialutil import Timeout
import serial.tools.list_ports
import serial
import os

from datetime import datetime
import time

# DEBUG = True
DEBUG = False

def timestamp():
        # gives current time in a format HH:MM:SS-dd/mm/yyyy
        return datetime.now().strftime("%H:%M:%S.%f")[:-3]

class SerialCom:

    COM_PORT=''
    BAUDRATE='115200'

    @staticmethod
    def return_open_ports():
        # print(serial.tools.list_ports)
        list_of_open_ports = serial.tools.list_ports.comports()
        return list_of_open_ports

    def establish_communication(self, com_port, baudrate):
        try:
            com_line = serial.Serial(port=com_port, 
                                    baudrate=self.serial_baudrate,
                                    timeout=2)
            return com_line
        except:
            print("failed to establish communication")
            return 'connection-failed'

#   auto finds correct COM port for arduino device.  
    def find_correct_port(self, baudrate, connection_token): 
        open_ports = self.return_open_ports()
        if open_ports != None:
            for port in open_ports:
                communication_line = self.establish_communication(port.device, baudrate) 
                #try to talk with all open COM ports
                if communication_line != 'connection-failed':                  
                    # if connection was success, proceed
                    print(f"trying connection with {port.device}")
                    while True:
                        data = communication_line.readline()
                        data = data.decode(encoding="utf-8", errors="replace").strip()
                        print(data)
                        if data == connection_token:
                            print(f"connection secured with {port.device}")
                            return port.device, communication_line
                        else:
                            print('wrong device')
                            break
        return None, None

    # creates an instance of communication with centigrade arduino station
    def __init__(self, serial_baudrate='115200'):
        self.serial_baudrate = serial_baudrate
        self.com_port, self.communication_line = self.find_correct_port(self.serial_baudrate, '000')
        if self.communication_line != None:
            self.connection_established = True
        else:
            self.connection_established = False

    # not used anymore
    def instruction_case(self, instruction=None):
        return {
            'get_closer':'c',
            'measure_temp':'m',
            'high_temperature':'h',
            'normal_temperature':'n',
            'up':'u',
            'down':'d',
            'right':'r',
            'left':'l',
            'closer':'c',
            'further':'f',
        }.get(instruction, '-')

    def receive_serial_data(self):
        data_received = self.communication_line.readline()
        decoded_data = data_received.decode(encoding="utf-8", errors="replace").strip()
        return decoded_data


    # not used anymore
    def send_serial_data(self, data_to_send):
        instruction = self.instruction_case(data_to_send)
        if instruction != '-':
            data_to_send = instruction
        data = bytes(str(data_to_send), encoding="utf-8")
        self.communication_line.write(data)



print(f'{__name__}.py imported...')


if DEBUG:
    print(SerialCom().return_open_ports())
    arduino = SerialCom()

    while True:
        # time.sleep(0.1)
        print(f"{timestamp()} {type(arduino.receive_serial_data())}")





