import fitbit
import datetime
import gather_keys_oauth2 as Oauth2

CLIENT_ID = '22CTVH'
CLIENT_SECRET = '90dca659ed79208397b8cb3f3682f4f4'

server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
server.browser_authorize()
ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])

client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, oauth2=True,
                       access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)

today = str(datetime.datetime.now().strftime("%Y-%m-%d"))
yesterday = str((datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d"))

fit_statsHR = client.intraday_time_series('activities/heart', base_date=yesterday, detail_level='15min')


print('restingHeartRate:', type(fit_statsHR['activities-heart']))

for item in fit_statsHR['activities-heart']:
    print(type(item), str(item))

for item in fit_statsHR['activities-heart']:
    for thing in item:
        print(thing)

print(fit_statsHR['activities-heart'][0]['value']['restingHeartRate'])

print(len(fit_statsHR['activities-heart'][0]['value']))

fit_statsHR = client.intraday_time_series('activities/heart', base_date=today, detail_level='15min')

print(len(fit_statsHR['activities-heart'][0]['value']))

