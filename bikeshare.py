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
    print("Hello! Let's explore some US bikeshare data!")
    
    # Get user input for city (Chicago, New York City, Washington)
    city = input("Enter the city (Chicago, New York City, Washington): ").lower()
    while city not in ['chicago', 'new york city', 'washington']:
        city = input("Choose between Chicago, New York City, or Washington: ").lower()

    # Get user input for month (All, January, February, ..., June)
    month = input("Enter month (All, January, February, March, April, May, June): ").lower()
    while month not in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
        month = input("Enter month (All, January, February, March, April, May, June): ").lower()

    # Get user input for day of week (All, Monday, Tuesday, ... Sunday)
    day = input("Enter day (All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday): ").lower()
    while day not in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
        day = input("Enter day (All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday): ").lower()

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
    # Load intended file into data frame
    df = pd.read_csv('{}.csv'.format(city))

    # Convert columns of Start Time and End Time into date format yyyy-mm-dd
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # Extract month from Start Time into new column called month
    df['month'] = df['Start Time'].dt.month

    # Filter by month
    if month != 'all':
        # Use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # Filter by month to create the new dataframe
        df = df[df['month'] == month]

    # Extract day from Start Time into new column called day_of_week
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()

    # Filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    print("The most common month is:", df['month'].mode()[0])

    # Display the most common day of week
    print("The most common day is:", df['day_of_week'].mode()[0].title())

    # Display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print("The most common start hour is:", df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    print("The most common start station is:", df['Start Station'].mode()[0])

    # Display most commonly used end station
    print("The most common end station is:", df['End Station'].mode()[0])

    # Display most frequent combination of start station and end station trip
    print("The most frequent combination of start and end stations is:")
    most_common_start_and_end_stations = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print(most_common_start_and_end_stations)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_duration = df['Trip Duration'].sum() / 3600.0
    print("Total travel time in hours is:", total_duration)

    # Display mean travel time
    mean_duration = df['Trip Duration'].mean() / 3600.0
    print("Mean travel time in hours is:", mean_duration)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("User types:\n", user_types)
    
    # Check if 'Gender' column is available
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print("\nGender counts:\n", gender_counts)
    else:
        print("\nGender data is not available for this city.")
    
    # Check if 'Birth Year' column is available
    if 'Birth Year' in df.columns:
        earliest_year = int(df['Birth Year'].min())
        most_recent_year = int(df['Birth Year'].max())
        most_common_year = int(df['Birth Year'].mode()[0])
        print(f"\nBirth Year stats:\nEarliest: {earliest_year}\nMost recent: {most_recent_year}\nMost common: {most_common_year}")
    else:
        print("\nBirth Year data is not available for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def raw_data(df):
    """Displays raw data in increments of 5 rows based on user input."""
    print("Press Enter to see 5 rows of raw data, or type 'no' to skip.")
    x = 0
    while input().lower() != 'no':
        x += 5
        print(df.head(x))

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
