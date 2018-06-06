import fitbit
import datetime
import gather_keys_oauth2 as oauth2
import numpy


# Generate formula time string.
def generate_date(days):
    return str((datetime.datetime.now() - datetime.timedelta(days=days)).strftime("%Y-%m-%d"))


# Get averange rest hear beat rate from fitbit server.
def get_averange_hbt_from_server(client_id, client_secret, days):
    # If the input days are wrong return -1.
    if days < 1 and isinstance(days, int):
        print("Wrong input days.")
        return -1

    rest_hbr_list = []

    # Initialize sever connection.
    server = oauth2.OAuth2Server(client_id, client_secret)
    server.browser_authorize()
    access_token = str(server.fitbit.client.session.token['access_token'])
    refresh_token = str(server.fitbit.client.session.token['refresh_token'])

    client = fitbit.Fitbit(client_id, client_secret, oauth2=True,
                           access_token=access_token, refresh_token=refresh_token)

    # Get the rest heartbeat rate data of few days before.
    for day in range(1, days):
        fit_stats_hr = client.intraday_time_series(
            'activities/heart', base_date=generate_date(day), detail_level='15min')

        values = fit_stats_hr['activities-heart'][0]['value']
        if 'restingHeartRate' in values:
            rest_hbr_list.append(values['restingHeartRate'])
            print("Date: %s, Rest heartbeat rate: %d" %
                  (fit_stats_hr['activities-heart'][0]['dateTime'], values['restingHeartRate']))

    # Get averange.
    if len(rest_hbr_list) != 0:
        result = numpy.mean(rest_hbr_list)
        print("Got averange HBR data from fitbit server: ", result)
        return result
    else:
        return -1


if __name__ == '__main__':
    CLIENT_ID = '22CTVH'
    CLIENT_SECRET = '90dca659ed79208397b8cb3f3682f4f4'

    print(get_averange_hbt_from_server(CLIENT_ID, CLIENT_SECRET, 7))
