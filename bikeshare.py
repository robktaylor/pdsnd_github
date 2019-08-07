import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities = ['Chicago', 'Washington', 'New York City']
    city = input('\nPlease enter the name of the city you would like to learn more about.\nYou can choose between Chicago, Washington or New York City: ').title()
    while city not in cities:
        city = input('\nPlease try again.\nYou can choose between Chicago, Washington or New York City: ').title()

    # TO DO: get user input for month (all, january, february, ... , june)
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'All']
    month = input('\nFor what month would you like to learn more?\nPlease select either January, February, March, April, May or June.\nOr you can select \"All\" to see all months together: ').title()
    while month not in months:
        month = input('\nPlease try again.\nPlease select either January, February, March, April, May or June. Or you can select \"All\": ').title()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'All']
    day = input('\nFor what day of the week would you like to learn more?\nPlease select either Sunday, Monday, Tuesday, Wednesday, Thursday, Friday or Saturday.\nOr you can select \"All\" to see all days together: ').title()
    while day not in days:
        day = input('\nPlease try again.\nPlease select either Sunday, Monday, Tuesday, Wednesday, Thursday, Friday or Saturday. Or you can select \"All\": ').title()

    if month == 'All' and day != 'All':
        print('\nYou\'ve selected to see data on {} over all months on {}s. Let\'s get started.'.format(city, day))
    elif day == 'All' and month != 'All':
        print('\nYou\'ve selected to see data on {} for the month of {} every day of the week. Let\'s get started.'.format(city, month))
    elif day == 'All' and month == 'All':
        print('\nYou\'ve selected to see data on {} for every month on every day of the week. Let\'s get started.'.format(city))
    else:
        print('\nYou\'ve selected to see data on {} for the month of {} on {}s. Let\'s get started.'.format(city, month, day))

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    months = {'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6}
    df = pd.read_csv(CITY_DATA[city.lower()])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    if month != 'All':
        df = df[df['Start Time'].dt.month == months[month]]
    if day != 'All':
        df = df[df['Start Time'].dt.weekday_name == day]
    #print(df)

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    if month == 'All':
        most_common_month = df['Start Time'].dt.month.mode()-1
        message_month = 'The most common month for travelling is {}.'.format(months[most_common_month[0]])
    else:
        message_month = 'Displaying the most common month for travel is not available when a month is selected in the data filter.'

    print(message_month)

    # TO DO: display the most common day of week
    if month == 'All' and day == 'All':
        most_common_day = df['Start Time'].dt.weekday_name.mode()
        message_day = 'The most common day of the week for travelling is {}.'.format(most_common_day[0])
    elif month != 'All' and day == 'All':
        most_common_day = df['Start Time'].dt.weekday_name.mode()
        message_day = 'The most common day of the week for travelling in {} is {}.'.format(month, most_common_day[0])
    else:
        message_day = 'Displaying the most common day of the week for travel is not available when a day is selected in the data filter.'

    print(message_day)

    # TO DO: display the most common start hour
    most_common_hour = df['Start Time'].dt.hour.mode()
    hour = most_common_hour[0]
    if hour == 0:
        hour = 12
        morn_or_aft = 'am'
    elif hour < 12:
        morn_or_aft = 'am'
    elif hour == 12:
        morn_or_aft = 'pm'
    elif hour > 12:
        hour -= 12
        morn_or_aft = 'pm'

    message_hour = 'The most common hour for starting travel is {}{}.'.format(hour, morn_or_aft)

    print(message_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df, month, day):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('The most common starting station of travellers is {}.'.format(most_common_start_station))

    # TO DO: display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('The station that is the most common destination of travellers is {}.'.format(most_common_end_station))

    # TO DO: display most frequent combination of start station and end station trip
    if month == 'All' or day == 'All':
        df['Trip'] = df['Start Station'] + ' to ' + df['End Station']
        most_common_trip = df['Trip'].mode()[0]
        print('\nThe most common trip taken by users was from {}\n'.format(df['Trip'].mode()[0]))
    else:
        start_station = list(df['Start Station'])
        end_station = list(df['End Station'])
        stations = list(zip(start_station, end_station))
        trips = {}

        for trip in stations:
            if trip not in trips:
                trips[trip] = 1
            else:
                trips[trip] += 1

        for names, number in trips.items():
            if number == max(trips.values()):
                name_1 = names[0]
                name_2 = names[1]
                times = number

        print('\nThe most common trip taken by users was from {} to {}. \nThis trip was completed {} times.'.format(name_1, name_2, times))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    ttl_travel_time = df['Trip Duration'].sum()
    ttl_travel_time_hours = int(ttl_travel_time // 3600)
    ttl_travel_time_minutes = int((ttl_travel_time % 3600) // 60)
    ttl_travel_time_seconds = int(((ttl_travel_time % 3600) % 60))

    message_ttl = 'The total travel time for this period is {} hours, {} minutes and {} seconds.'.format(ttl_travel_time_hours, ttl_travel_time_minutes, ttl_travel_time_seconds)

    print(message_ttl)

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    mean_travel_time_hours = int(mean_travel_time // 3600)
    mean_travel_time_minutes = int((mean_travel_time % 3600) // 60)
    mean_travel_time_seconds = int(((mean_travel_time % 3600) // 60))

    message_mean = 'The mean travel time for this period is {} hours, {} minutes and {} seconds.'.format(mean_travel_time_hours, mean_travel_time_minutes, mean_travel_time_seconds)

    print(message_mean)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print('The following details the User Type of travellers and the number of each:')

    users = list(df['User Type'])
    whom = {}

    for who in users:
        if who not in whom:
            whom[who] = 1
        else:
            whom[who] += 1

    for whos, number in whom.items():
        print(whos, ':', number)

    # TO DO: Display counts of gender
    if city.lower() != 'washington':
        print('\nThe following details the gender of travellers and the number of each:')

        genders = list(df['Gender'])
        pronoun = {}

        for what in genders:
            if what not in pronoun:
                pronoun[what] = 1
            else:
                pronoun[what] += 1

        for whats, number in pronoun.items():
            print(whats, ':', number)

    # TO DO: Display earliest, most recent, and most common year of birth
        ealiest = int(min(df['Birth Year']))
        latest = int(max(df['Birth Year']))
        most_common = int(df['Birth Year'].mode())

        print('\nThe ealiest year of birth of users is: {}'.format(ealiest))
        print('The most recent year of birth of users is: {}'.format(latest))
        print('The most common year of birth of users is: {}'.format(most_common))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw(df):
    """

    Asks the user if they want to see the raw data from their query. If the
    user types 'yes', this code displays 5 lines of raw data. The code asks the
    user again if they want to see 5 more lines of raw data, and shall
    continue to do so until the user types an answer other than 'yes'.

    """
    index = 0
    while True:
        see_data = input('\nDo you want to see the raw data from the statistics displayed above? Enter yes or no.\n')
        if see_data.lower() == 'yes':
            print(df.iloc[index:(index + 5)])
            index += 5
        elif see_data.lower() != 'yes':
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df, month, day)
        trip_duration_stats(df)
        user_stats(df, city)
        raw(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
