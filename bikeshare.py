import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


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
    city = input('\nWhich city do you want to see its data? chicago, new york city or washington\n')
    city_list = ['chicago', 'new york city', 'washington']
    while city.lower() not in city_list:
        city = input('\nThe name you entered didn\'t match any of the three cities'
                     '\nPlease choose either chicago, new york city or washington').lower()

    # TO DO: get user input for month (all, january, february, ... , june)

    month = input('\nWhich month do you want to see its data?\n'
                  'january, february, march, april, may, june or all\n').lower()
    months_list = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while month.lower() not in months_list:
        month = input('\nThe name you entered didn\'t match any of the months'
                      '\nPlease choose either january, february, march, april, may, june or all\n').lower()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('\nWhich day do you want to see its data?'
                '\nsaturday, sunday, monday, tuesday, wednesday, thursday, friday or all\n').lower()
    days_list = ['saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'all']
    while day.lower() not in days_list:
        day = input('\nThe name you entered didn\'t match any of the days'
                    '\nPlease choose either saturday, sunday, monday, tuesday, wednesday, thursday, friday or all').lower()

    print('-' * 40)
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
    df = pd.read_csv('{}'.format(city.replace(' ', '_') + '.csv'))

    # edit Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # edit End Time column to datetime
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month from Start Time to create new column
    df['month'] = df['Start Time'].apply(lambda x: x.month)

    # extract day from Start Time to create new column
    df['day_of_week'] = df['Start Time'].apply(lambda x: x.strftime('%A').lower())

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df.loc[df['month'] == month, :]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df.loc[df['day_of_week'] == day, :]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    print('\nMost common month is:{}'.format(str(df['month'].mode()[0])))

    # TO DO: display the most common day of week
    print('\nMost common day of the week is:{}'.format(str(df['day_of_week'].mode()[0])))

    # TO DO: display the most common start hour
    # extract hour from Start Time to create new column
    df['start_hour'] = df['Start Time'].dt.hour
    print('\nMost common hour of the day is:{}'.format(str(df['start_hour'].mode()[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('\nMost commonly used start station is: {}'.format(df['Start Station'].mode()[0]))

    # TO DO: display most commonly used end station
    print('\nMost commonly used end station is: {}'.format(df['End Station'].mode()[0]))

    # TO DO: display most frequent combination of start station and end station trip
    # create combined start and end station column
    df['combined'] = df['Start Station'] + ' to ' + df['End Station']
    print('\nMost common route is: {}'.format(df['combined'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    # create duration of travel column
    df['Duration'] = df['End Time'] - df['Start Time']
    print('\nTotal travel time is: {}'.format(str(df['Duration'].sum())))

    # TO DO: display mean travel time
    print('\nAverage travel time is: {}'.format(str(df['Duration'].mean().round('1s'))))

    print("\nThis took %s seconds. {}" % (time.time() - start_time))
    print('-' * 40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    types_of_users = df['User Type'].value_counts().sort_values()
    print('\nUser types are:'
          '\nCustomers: {}'
          '\nSubscribers: {}'.format(types_of_users[0], types_of_users[1]))

    # TO DO: Display counts of gender
    if city != 'washington':
        gender_type = df['Gender'].value_counts().sort_values()
        print('\nGender counts are:'
              '\nFemales: {}'
              '\nMales: {}'.format(gender_type[0], gender_type[1]))

    # TO DO: Display earliest, most recent, and most common year of birth
    if city != 'washington':
        print('\nEarliest year of birth is:{}'.format(str(int(df['Birth Year'].min()))))
        print('\nMost recent year of birth is: {}'.format(str(int(df['Birth Year'].max()))))
        print('\nAnd most common year of birth is: {}'.format(str(int(df['Birth Year'].mode()[0]))))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def repeat(df):
    start_line = 0
    end_line = 5

    message = input("\nDo you wish to see the raw data?:"
                           "\nPlease choose yes or no\n").lower()

    if message == 'yes':
        while end_line <= df.shape[0] - 1:

            print(df.iloc[start_line:end_line, :])
            start_line += 5
            end_line += 5

            end_message = input("Do you wish to continue?\n").lower()
            if end_message == 'no':
                break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        repeat(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
