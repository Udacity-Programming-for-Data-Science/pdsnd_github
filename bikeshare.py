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
    city = ''
    city = input("Which city data are you interested? Please select one from 'chicago', 'new york city', and 'washington'. ")
    while city not in ('chicago', 'new york city', 'washington'):
        city = input("Invalid city name, please re-enter. ")

    # TO DO: get user input for month (all, january, february, ... , june)
    month = ''
    month = input('Select name of the month to filter by, or "all" to apply no month filter (lower case): ')
    while month not in ('all', 'january', 'february', 'march', 'april', 'may', 'june'):
        month = input("Wrong option. Please select within 'all', 'january', 'february', 'march', 'april', 'may', 'june': ")

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    day = input('Select name of the day to filter by, or "all" to apply no day filter (lower case): ')
    while day not in ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
        day = input("Wrong option. Please enter the right day of week: ")

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
    
    # pre-process the dataframe for conveniently analyze the data later
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        df = df[df['day'] == day.title()]
    #print(df[1: 5])
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    month = months[df.month.mode()[0] - 1]
    print("The most common month is: " + month + "\n")

    # TO DO: display the most common day of week. Formatting the output to increase readability.
    print("The most common day of week is: {} \n".format(df.day.mode()[0]))
    
    # TO DO: display the most common start hour
    print("The most common hour is: " + str(df.hour.mode()[0]) + "\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print("The most common start station is: " + df['Start Station'].mode()[0] + "\n")

    # TO DO: display most commonly used end station
    print("The most common end station is: " + df['End Station'].mode()[0] + "\n")

    # TO DO: display most frequent combination of start station and end station trip
    df['Start - End Station Combination'] = "\nSTART: " + df['Start Station'] + "\nEND: " + df['End Station']
    print("The most common start - end station combination is: " + df['Start - End Station Combination'].mode()[0] + "\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # [Updated] TO DO: display total travel time. Format the result for better readability.
    total_trip_duration = time_converter(df['Trip Duration'].sum())
    print_results("Total travel time: ", total_trip_duration, "\n")

    # [Updated] TO DO: display mean travel time. Format the result for better readability.
    mean_trip_duration = time_converter(df['Trip Duration'].mean())
    print_results("Average travel time: ", mean_trip_duration, "\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print_results("Count of user types: ", "{:,}".format(df['User Type'].count()))

    # [Updated] Washington, D.C. doesn't have gender or birth year data, adding try - except to avoid errors
    try:
        # TO DO: Display counts of gender
        print_results("Count of genders: ", "{:,}".format(df['Gender'].count()))

        # TO DO: Display earliest, most recent, and most common year of birth
        print_results("Earliest year of birth: ", str(df['Birth Year'].min()))
        print_results("Most recent year of birth: ", str(df['Birth Year'].max()))
        print_results("Most common year of birth: ", str(df['Birth Year'].mode()[0]))
        
    except:
        print("No gender or birth year data available for this city.")
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def print_results(text1, result, text2 = ''):
    """
    Concat text and results and print out the final results. Streamline the process
        
    Args:
        (str)text1 - First piece of output 
        (str)result - Calculated variables to be showcased, needs to be converted to string format beforehand
        (str)text2 (optional) - End of output (if needed)
    Returns: 
        Printing - The printing of desired results
    """
    
    print(text1 + result + text2 + "\n")
   
# [Updated] Added time converter function to reduce duplicated codes
def time_converter(time):
    m, s = divmod(time, 60)
    h, m = divmod(m, 60)
    print_text = str(s) + 's'
    if m > 0:
        print_text = str(m) + 'm ' + print_text
        if h > 0:
            print_text = str(h) + 'h ' + print_text
    return print_text
    
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
                  
        # [Updated] Check with user whether showcase the first 5 rows of raw data. Keep asking until 1. user selects no, and 2. rows are exhausted
        display_raw_data = input("Do you want to check the first 5 rows of the raw data? yes/no \n")
        start_row = 0
        while display_raw_data not in ("yes", "no"):
            display_raw_data = input("Invalid input. Please input yes or no. \n")
        while display_raw_data == "yes":
            printed_rows = df[start_row : start_row + 5]
            if printed_rows.empty:
                  print("No more rows")
                  break
            print(printed_rows)
            display_raw_data = input("Do you want to check the next 5 rows of the raw data? yes/no \n")
            while display_raw_data not in ("yes", "no"):
                display_raw_data = input("Invalid input. Please input yes or no. \n")
            start_row += 5
            
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
