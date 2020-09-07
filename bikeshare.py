import time
import pandas as pd
import numpy as np
#libraries/modules consisting of additional functions to make this script and my life easier
"""commit  1"""

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

#month list for get_filters
MONTH_DATA = ('january', 'february', 'march', 'april', 'may', 'june', 'all')

#day of the week list for get_filters
DAY_DATA = ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday',
'saturday', 'all')

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month
        filter
        (str) day - name of the day of week to filter by, or "all" to apply no
        day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    #get user input for city (chicago, new york city, washington)
    city = None
    while city not in CITY_DATA.keys():
        city = input("Would you like to see data for Chicago, New York City, or Washington? ").lower()
        if city not in CITY_DATA.keys():
            print("\nUnacceptable input. Try again.\n")
            continue
        else:
            break


    #get user input for month filter (all, january, february, ... , june)
    while True:
        month = input("Select month filter, or enter 'all' for no filter. ").lower()
        if month not in MONTH_DATA:
            print("\nUnacceptable input. Try again.\n")
            continue
        else:
            break

    #get user input for day of week filter (all, monday, tuesday, ... sunday)
    while True:
        day = input("Select day of the week filter, or say 'all' for no filter. ").lower()
        if day not in DAY_DATA:
            print("\nUnacceptable input. Try again.\n")
            continue
        else:
            break


    print('-'*120)
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def raw_data(df):
    """Asks user if they want to see raw data. Then displays 5 lines \
    of raw data. Upon repeat requests, displays next 5 lines of raw data"""

    show_data = input("Firstly, would you like to see 5 rows of raw data? \
    Enter 'yes' to continue, 'no' to skip. \n").lower()

    i = 0 #initialises row for data display

    while True:
        if show_data.lower() != 'no':
            print(df.iloc[i:(i + 5), 1:-2]) #show relevant index and rows
            i += 5
            print('-'*120) #lines to break data displays. Improves readability
            show_data = input("\nSee 5 more rows of raw data? Enter 'yes' to \
            see, 'no' to skip. ").lower()
        else:
            break
    print('-'*120)
    return


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #display the most common month
    df['cmonth'] = df['Start Time'].dt.month
    popular_month = df['cmonth'].mode()[0]
    print('\nMost common month:', popular_month)

    #display the most common day of week
    df['cweekday_name'] = df['Start Time'].dt.weekday_name
    popular_weekday_name = df['cweekday_name'].mode()[0]
    print('\nMost common day of the week:', popular_weekday_name)

    #display the most common start hour
    df['chour'] = df['Start Time'].dt.hour
    popular_hour = df['chour'].mode()[0]
    print('\nMost common start hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('\nMost common start station:', popular_start_station)

    #display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('\nMost common end station:', popular_end_station)

    #display most frequent combination of start station and end station trip
    df['Popular_Trip'] = df['Start Station'] + ' to ' + df['End Station']
    popular_trip = df['Popular_Trip'].mode()[0]
    print('\nMost common trip:', popular_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #display total travel time
    sum_travel = df['Trip Duration'].sum()
    print('\nTotal travel time is', sum_travel)

    #display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print('\nMean travel time is', mean_travel)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Display counts of user types
    user_types = df['User Type'].value_counts()
    print('\nThere are {} subscribers and {} customers.'.format(user_types[0], user_types[1]))

    #Inform of missing data columns for Washington
    if city == 'washington':
        print("\nNo gender or birth data for this city. ")
    else:

    #Display counts of gender
        gender = df['Gender'].value_counts()
        print('\nThere are {} males and {} females.'.format(gender[0], gender[1]))

    #Display earliest, most recent, and most common year of birth
        min_birth = df['Birth Year'].min()
        max_birth = df['Birth Year'].max()
        common_birth = df['Birth Year'].mode()[0]
        print('\nEarliest birth year is {}. \nMost recent birth year is {}. \
        \nMost common birth year is {}.'.format(min_birth, max_birth, common_birth))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
