import time
from datetime import date
import sys
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def user_input_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city=str(input("Please enter CITY name you want the analysis for:\nchicago, new york, or washington?\n")).lower()
    while city not in CITY_DATA.keys():
        city=str(input('Invalied input! Please type the correct city name:\n(chicago / new york / washington).\n')).lower()
        
    # get user input for month (all, january, february, ... , june)
    month=str(input("Type MONTH name if you want to filter by a specific month.\nIf not, print 'all'.\n")).lower()
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while month not in months:
        month=str(input('Please enter a valid month!.\nNotice that our data is collected through january to june.\n')).lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day_names=['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'All']
    day=str(input("Whould you like to filter by DAY? Type it.\nIf not, print 'all'.\n"))
    while day.title() not in day_names:
        day=str(input('Please enter a valid Day Name!. Follow this format:\nSaturday, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday.\n'))

    print('Got your preferences ;)')
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
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour']= df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        for i in months:
            if month == i:
                month = months.index(i) + 1 
        # filter by month to create the new dataframe
        df = df[df['month']==month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']==day.title()] 
    print('Awesome! let\'s bake data ;)')
    return df


def time_stats(df,month,day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month in case we didn't filter by a specific one
    if month == 'all':
      month_dict={1:'january', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June'}
      most_common_month= df['month'].mode()[0]
      print('the most common month of travel is: ', month_dict[most_common_month])

    # display the most common day of week in case we didn't filter by a specific one
    if day == 'all':
      most_common_day = df['day_of_week'].mode()[0]
      print('the most common day of travel during {} month/s is: {}.'.format(month, most_common_day))

    # display the most common start hour
    most_common_hour = df['hour'].mode()[0]
    print('the most common hour of travel during {} month/s and {} day/s is: {}.'.format(month.title(), day.title(), most_common_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('Quite good! --- There\'s more:')


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('the most common start station is: ', most_common_start_station)

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('the most common end station is: ', most_common_end_station)

    # display most frequent combination of start station and end station trip
    trip_count=pd.Series(df.groupby(['Start Station','End Station'])['Start Station'].count())
    for i in trip_count.keys():
     if trip_count[i]==trip_count.max():
        most_frequent_trip= i
        no_of_trips=trip_count[i]
        print('The most frequent trip line is:\n{} with {} trip.'.format(most_frequent_trip, no_of_trips))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('Great! -_-')


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    #Convert End Time to a datetime format such as we did with Start Time
    df['End Time'] = pd.to_datetime(df['End Time'])

    # display total travel time
    travel_time= df['End Time'] - df['Start Time']
    total_travel_time= travel_time.sum()
    print('Total trips duration is: ',total_travel_time)

    # display mean travel time
    mean_trip_duration= travel_time.mean()
    print('Average trip duration is: ',mean_trip_duration)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types= df['User Type'].value_counts()
    print('User types Count is:\n',user_types)

    # Display counts of gender in NYC or Chicago
    if city != 'washington':
        gender_count= df['Gender'].value_counts()
        print('Users gender Count is:\n{}\n'.format(gender_count))
        # Display youngest, oldest, average, and most common user age ranges
        todays_date = date.today()
        oldest_age = date.today().year - df['Birth Year'].min()
        youngest_age = date.today().year - df['Birth Year'].max()
        average_age_range = date.today().year - int(df['Birth Year'].mean())
        most_frequent_age = date.today().year - df['Birth Year'].mode()[0]
        print('Users ages range between: {} and {} years old.'.format(youngest_age,oldest_age))
        print('Users average age range is: {} years old.'.format(average_age_range))
        print('And the most frequent user age is: {} years old.'.format(most_frequent_age))
    else:
        print('That\'s all for users here..\nwashington DataSet doesn\'t provide Gender/birth data.')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
def view_raw_data(df):
    """  Asks users if they want to see 5 lines of raw data,
      Display that data if the answer is 'yes', Continue iterating these prompts
      and displaying the next 5 lines of raw data at each iteration,Stop the program
      when the user says 'no' or there is no more raw data to display."""
    i=0
    user_select=input('So after having a look at these statistics,\nWhould you like to see a sample of our raw data? Type yes/no:\n')
    while True and i<= df.shape[0]:
        if user_select == 'yes':
          print(df[i:i+5])
          i+=5
          user_select=input('Want to see more data?\n')
        else:
            break
          
def main():
    while True:
        city, month, day = user_input_filters()
        df = load_data(city, month, day)

        time_stats(df,month,day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        view_raw_data(df)

        restart = input('End of script :)\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
