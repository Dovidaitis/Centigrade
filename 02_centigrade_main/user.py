
class User():

    @staticmethod
    def decode_user_data(data_to_decode):
        data = data_to_decode.split("-")
        distance = int(data[0]) # distance from user face to sensor in centimeters
        temperature = float(data[1])
        rfid = data[2]
        return distance, temperature, rfid

    def __init__(self, user_data):
        self.distance, self.temperature, self.rfid,  = self.decode_user_data(user_data)


