import time
import pandas as pd
import numpy as np

# Constants for city data files
CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

# Valid options for months and days
VALID_MONTHS = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
VALID_DAYS = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

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
    while city not in CITY_DATA.keys():
        city = input("Choose between Chicago, New York City, or Washington: ").lower()

    # Get user input for month (All, January, February, ..., June)
    month = input("Enter month (All, January, February, March, April, May, June): ").lower()
    while month not in VALID_MONTHS:
        month = input("Enter a valid month (All, January, February, ..., June): ").lower()

    # Get user input for day of week (All, Monday, Tuesday, ... Sunday)
    day = input("Enter day (All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday): ").lower()
    while day not in VALID_DAYS:
        day = input("Enter a valid day (All, Monday, Tuesday, ..., Sunday): ").lower()

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
        data_frame - Pandas DataFrame containing city data filtered by month and day
    """
    # Load the intended file into data frame
    data_frame = pd.read_csv(CITY_DATA[city])

    # Convert columns of Start Time and End Time into datetime format
    data_frame['Start Time'] = pd.to_datetime(data_frame['Start Time'])
    data_frame['End Time'] = pd.to_datetime(data_frame['End Time'])

    # Extract month from Start Time into new column called month
    data_frame['month'] = data_frame['Start Time'].dt.month

    # Filter by month if specified
    if month != 'all':
        # Use the index of the VALID_MONTHS list to get the corresponding int
        month = VALID_MONTHS.index(month) + 1
        data_frame = data_frame[data_frame['month'] == month]

    # Extract day from Start Time into new column called day_of_week
    data_frame['day_of_week'] = data_frame['Start Time'].dt.day_name().str.lower()

    # Filter by day of week if specified
    if day != 'all':
        data_frame = data_frame[data_frame['day_of_week'] == day]

    return data_frame

def time_stats(data_frame):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    print("The most common month is:", data_frame['month'].mode()[0])

    # Display the most common day of week
    print("The most common day is:", data_frame['day_of_week'].mode()[0].title())

    # Display the most common start hour
    data_frame['hour'] = data_frame['Start Time'].dt.hour
    print("The most common start hour is:", data_frame['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def station_stats(data_frame):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    print("The most common start station is:", data_frame['Start Station'].mode()[0])

    # Display most commonly used end station
    print("The most common end station is:", data_frame['End Station'].mode()[0])

    # Display most frequent combination of start station and end station trip
    print("The most frequent combination of start and end stations is:")
    most_common_stations = data_frame.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print(most_common_stations)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def trip_duration_stats(data_frame):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time in hours
    total_duration = data_frame['Trip Duration'].sum() / 3600.0
    print("Total travel time in hours is:", total_duration)

    # Display mean travel time in hours
    mean_duration = data_frame['Trip Duration'].mean() / 3600.0
    print("Mean travel time in hours is:", mean_duration)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def user_stats(data_frame):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = data_frame['User Type'].value_counts()
    print("User types:\n", user_types)
    
    # Check if 'Gender' column is available
    if 'Gender' in data_frame.columns:
        gender_counts = data_frame['Gender'].value_counts()
        print("\nGender counts:\n", gender_counts)
    else:
        print("\nGender data is not available for this city.")
    
    # Check if 'Birth Year' column is available
    if 'Birth Year' in data_frame.columns:
        earliest_year = int(data_frame['Birth Year'].min())
        most_recent_year = int(data_frame['Birth Year'].max())
        most_common_year = int(data_frame['Birth Year'].mode()[0])
        print(f"\nBirth Year stats:\nEarliest: {earliest_year}\nMost recent: {most_recent_year}\nMost common: {most_common_year}")
    else:
        print("\nBirth Year data is not available for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)
    
def raw_data(data_frame):
    """Displays raw data in increments of 5 rows based on user input."""
    print("Press Enter to see 5 rows of raw data, or type 'no' to skip.")
    rows_displayed = 0
    while input().lower() != 'no':
        rows_displayed += 5
        print(data_frame.head(rows_displayed))

def main():
    while True:
        city, month, day = get_filters()
        data_frame = load_data(city, month, day)

        time_stats(data_frame)
        station_stats(data_frame)
        trip_duration_stats(data_frame)
        user_stats(data_frame)
        raw_data(data_frame)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
