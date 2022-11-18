import time
import pandas as pd
import numpy as np
import datetime 

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
# Define option 'all' with index = 0
CITY_OPTS = ['chicago', 'new york city', 'washington']
MONTH_OPTS = ['all', 'january', 'february', 'march', 'april', 'may','june']
DAY_OF_WEEK_OPTS = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = input('Please enter the city name: ').lower()
            if city in CITY_OPTS:
                break
            else:
                print('Invalid city. Please try again!')
        except KeyError:
            print('Error occurs. Please try again!')

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input('Please enter month: ').lower()
            if month in MONTH_OPTS:
                break
            else:
                print('Invalid month. Please try again!')
        except KeyError:
            print('Error occurs. Please try again!')        

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input('Please input day of week: ').lower()
            if day in DAY_OF_WEEK_OPTS:
                break
            else:
                print('Invalid day of week. Please try again!')
        except KeyError:
            print('Error occurs. Please try again!')

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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = (df['Start Time'].dt.day_name())
    df['hour'] = df['Start Time'].dt.hour
    df['trip'] = df['Start Station'] + ' to ' + df['End Station']

    # apply month filter
    if month != 'all':
        monthIndex = MONTH_OPTS.index(month)
        df = df[df['month']==monthIndex] 

    # apply day of week filter
    if day != 'all':
        dayTitle = day.title()
        df = df[df['day_of_week']==dayTitle]
            
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    if len(df.index) > 0:
        # display the most common month
        common_month = df['month'].mode()[0]
        print('The most common month is', MONTH_OPTS[common_month].title())

        # display the most common day of week
        common_day_of_week = df['day_of_week'].mode()[0]
        print('The most common day is', common_day_of_week.title())

        # display the most common start hour
        common_hour = df['hour'].mode()[0]
        print('The most common hour is', common_hour)
    else:
        print('There is no record with current filter')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    if len(df.index) > 0:
        # display most commonly used start station
        common_start = df['Start Station'].mode()[0]
        print('The most commonly used start station is',common_start)

        # display most commonly used end station
        common_end = df['End Station'].mode()[0]
        print('The most commonly used end station is', common_end)

        # display most frequent combination of start station and end station trip
        common_trip = df['trip'].mode()[0]
        print('The most frequent combination of start station and end station trip is', common_trip)
    else:
        print('There is no record with current filter')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    if len(df.index) > 0:
        try:
            # display total travel time
            total_trip_duration = df['Trip Duration'].sum()   
            print('Total travel time: %s'% str(datetime.timedelta(seconds = int(total_trip_duration))))

            # display mean travel time
            avg_travel_time = df['Trip Duration'].mean()
            print('The average travel time: %s.'% round(avg_travel_time, 1))
        except KeyError:
            print('Trip Duration stats cannot be calculated because Trip Duration does not appear in the dataframe')
    else:
        print('There is no record with current filter')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def print_value_counts(data):
    """Common function to print value_counts without dtype"""
    for i in range(len(data.index.values)):
            print(data.index.values[i], ' : ', list(data)[i])


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    if len(df.index) > 0:
        # Display counts of user types
        try:
            user_types_count = df['User Type'].value_counts()
            print('Counts of user types')
            print_value_counts(user_types_count)
        except KeyError:
            print('User Type stats cannot be calculated because User Type does not appear in the dataframe')

        # Display counts of 
        try:
            genders_count = df['Gender'].value_counts()
            print('Counts of gender:')
            print_value_counts(genders_count)
        except KeyError:
            print('Gender stats cannot be calculated because Gender does not appear in the dataframe')
       
        # Display earliest, most recent, and most common year of birth
        try:
            earliest_birth_year = df['Birth Year'].min()
            print('The earliest year of birth is %s' % int(earliest_birth_year))
            most_recent_year = df['Birth Year'].max()
            print('The most recent year of birth is %s' % int(most_recent_year))
            most_common_year = df['Birth Year'].mode()[0]
            print('The most common year of birth is %s' % int(most_common_year))
        except KeyError:
            print('Birth Year stats cannot be calculated because Birth Year does not appear in the dataframe')
    else:
        print('There is no record with current filter')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Displays 5 next lines of raw data"""
    view_input_five = input('\nWould you like to see next 5 rows of data? Please enter (y)es or no:').lower()
    start_loc = 0
    while view_input_five == 'yes' or view_input_five == 'y':                
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        view_input_five = input("Do you wish to continue?: ").lower()

def main():
    while True:
        city, month, day = get_filters()
        load_data('washington','all','monday').shape[0]
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
