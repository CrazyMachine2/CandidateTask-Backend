API_KEY = "50881c1bb15318f7f608bd26e8861879"
URL_TEMPLATE = 'https://api.openweathermap.org/data/2.5/weather?q=%s&appid={API_KEY}&units=%s'.format(
    API_KEY=API_KEY)
METRIC = 'metric'
IMPERIAL = 'imperial'
CITIES = ['Berlin', 'Leipzig', 'Frankfurt', 'Halle',
          'Sofia', 'Varna', 'Plovdiv', 'London', 'Madrid', 'Rome']
MAIN = 'main'
TEMPERATURE = 'temp'

MESSAGES = {
    'ALREADY_EXIST_MESSAGE': {'message': 'already exist'},
    'SUCCESS': {'message': 'success'},
    'UNSUCCESS': {'message': 'unsuccess'},
}
