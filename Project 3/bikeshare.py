import time
import pandas as pd
import numpy as np

#try to edit py file
#try to edit py file

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

months = ('january', 'february', 'march', 'april', 'may', 'june')

weekdays = ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday',
            'saturday')

columns = ('st')


def get_valid_input(prompt, choices=('y', 'n')):
    """Returns a valid input from the user given a set of possible answers."""

    while True:
        user_input = input(prompt).lower().strip()
        # Terminate the program if the input is 'end'
        if user_input == 'end':
            raise SystemExit
        # Check if the input is a single choice
        elif ',' not in user_input:
            if user_input in choices:
                break
        # Check if the input has multiple choices separated by commas
        elif ',' in user_input:
            user_input_list = [i.strip().lower() for i in user_input.split(',')]
            if all(choice in choices for choice in user_input_list):
                break

        prompt = ("\nInvalid input. Please enter a valid option:\n> ")

    return user_input


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - Name of the city/cities to analyze
        (str) month - Name of the month(s) to filter
        (str) day - Name of the day(s) of the week to filter
    """

    print("\nHello! \nLet's explore some US bikeshare data!\n")
    print("Type 'end' at any time to exit the program.\n")

    while True:
        city = get_valid_input("\nWhich city/cities? "
                               "New York City, Chicago, or Washington? Use commas:\n> "
                               , CITY_DATA.keys())
        month = get_valid_input("\nFrom month? January February March April May or June? Use commas:\n> "
        						, months)
        day = get_valid_input("\nWhich day? Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday? Use commas:\n> "
        						, weekdays)

        # Confirm data
        confirmation = get_valid_input("\nPlease confirm."
                                       "\n\n City(ies): {}\n Month(s): {}\n Weekday(s): {}\n\n"
                                       " [y] Yes\n [n] No\n\n> ".format(city, month, day))

        if confirmation == 'y':
            break
        else:
            print("\nTry again!")

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Load data for the specified filters of city(ies), month(s), and day(s) whenever applicable.

    Args:
        (str) city - name of the city(ies) to analyze
        (str) month - name of the month(s) to filter
        (str) day - name of the day(s) of week to filter

    Returns:
        df - Pandas DataFrame containing filtered data
    """

    print("\nCalculating for imput your choice...")
    start_time = time.time()

    # Filter the data according to the selected city filters
    if isinstance(city, list):
        df = pd.concat(map(lambda city: pd.read_csv(CITY_DATA[city]), city), sort=True)
        # Reorganize DataFrame columns after a city concat
        try:
            df = df.reindex(columns=['Unnamed: 0', 'Start Time', 'End Time',
                                     'Trip Duration', 'Start Station',
                                     'End Station', 'User Type', 'Gender',
                                     'Birth Year'])
        except Exception as e:
            print(f"An error occurred while reorganizing DataFrame columns: {e}")
    else:
        df = pd.read_csv(CITY_DATA[city])

    # Create columns
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Weekday'] = df['Start Time'].dt.day_name()
    df['Start Hour'] = df['Start Time'].dt.hour

    # Filter the data according to month and weekday into two new DataFrames
    if isinstance(month, list):
        df = pd.concat(map(lambda month: df[df['Month'] == (months.index(month) + 1)], month))
    else:
        df = df[df['Month'] == (months.index(month) + 1)]

    if isinstance(day, list):
        df = pd.concat(map(lambda day: df[df['Weekday'] == day.title()], day))
    else:
        df = df[df['Weekday'] == day.title()]

    print("\nThis took {:.2f} seconds.".format(time.time() - start_time))
    print('-' * 40)

    return df



def time_stats(df):
    """Display statistics on the most frequent times of travel.

    Args:
        df (DataFrame): DataFrame containing filtered data

    Returns:
        None
    """
    print('\nDisplaying the statistics on the most frequent times of travel...\n')
    start_time = time.time()

    # Display the most common month
    most_common_month = df['Month'].mode()[0]
    print('For the selected filter, the month with the most travels is: ' +
          str(months[most_common_month-1]).title() + '.')

    # Display the most common day of week
    most_common_day = df['Weekday'].mode()[0]
    print('For the selected filter, the most common day of the week is: ' +
          str(most_common_day) + '.')

    # Display the most common start hour
    most_common_hour = df['Start Hour'].mode()[0]
    print('For the selected filter, the most common start hour is: ' +
          str(most_common_hour) + '.')

    print("\nThis took {:.2f} seconds.".format(time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Display statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display the most commonly used start station
    most_common_start_station = str(df['Start Station'].mode()[0])
    print("The most common start station is: " + most_common_start_station)

    # Display the most commonly used end station
    most_common_end_station = str(df['End Station'].mode()[0])
    print("The most common end station is: " + most_common_end_station)

    # Display the most frequent combination of start station and end station trip
    df['Start-End Combination'] = df['Start Station'] + ' - ' + df['End Station']
    most_common_start_end_combination = str(df['Start-End Combination'].mode()[0])
    print("The most common start-end combination of stations is: " + most_common_start_end_combination)

    print("\nThis took {:.2f} seconds.".format(time.time() - start_time))
    print('-' * 40)
def trip_duration_stats(df):
    """Display statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Calculate total travel time in seconds
    total_travel_seconds = df['Trip Duration'].sum()

    # Convert total travel time to days, hours, minutes, and seconds
    days = total_travel_seconds // (24 * 3600)
    total_travel_seconds %= (24 * 3600)
    hours = total_travel_seconds // 3600
    total_travel_seconds %= 3600
    minutes = total_travel_seconds // 60
    seconds = total_travel_seconds % 60

    # display total travel time
    total_travel_time = f"{int(days)}d {int(hours)}h {int(minutes)}m {int(seconds)}s"
    print(f'The total travel time is: {total_travel_time}.')

    # Calculate mean travel time in seconds
    mean_travel_seconds = df['Trip Duration'].mean()

    # Convert mean travel time to minutes and seconds
    mean_minutes = int(mean_travel_seconds // 60)
    mean_seconds = int(mean_travel_seconds % 60)

    # display mean travel time
    mean_travel_time = f"{mean_minutes}m {mean_seconds}s"
    print(f"The mean travel time is: {mean_travel_time}.")

    print("\nThis took {:.2f} seconds.".format(time.time() - start_time))
    print('-' * 40)
    
def user_stats(df, city):
    """Display statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("User types:")
    print(user_types.to_string())

    # Display counts of gender if 'Gender' column exists
    if 'Gender' in df.columns:
        gender_distribution = df['Gender'].value_counts()
        print("\nDistribution for each gender:")
        print(gender_distribution.to_string())
    else:
        print("We're sorry! There is no data of user genders for {}."
              .format(city.title()))

    # Display earliest, most recent, and most common year of birth if 'Birth Year' column exists
    if 'Birth Year' in df.columns:
        try:
            earliest_birth_year = int(df['Birth Year'].min())
            print("\nFor the selected filter, the oldest person to ride one "
                  "bike was born in:", earliest_birth_year)
            
            most_recent_birth_year = int(df['Birth Year'].max())
            print("For the selected filter, the youngest person to ride one "
                  "bike was born in:", most_recent_birth_year)
            
            most_common_birth_year = int(df['Birth Year'].mode()[0])
            print("For the selected filter, the most common birth year amongst "
                  "riders is:", most_common_birth_year)
        except ValueError:
            print("There are no valid birth years in the data.")
    else:
        print("We're sorry! There is no data of birth year for {}."
              .format(city.title()))

    print("\nThis took {:.2f} seconds.".format(time.time() - start_time))
    print('-' * 40)
def raw_data(df, mark_place):
    """Display 5 lines of sorted raw data each time."""

    # Check if the user wants to continue from the last place
    if mark_place > 0:
        last_place = input("\nWould you like to continue from where you stopped last time? \n [y] Yes\n [n] No\n\n>").lower()
        if last_place == 'n':
            mark_place = 0

    # Sort data by column if starting from the beginning
    if mark_place == 0:
        while True:  
            sort_df = input("\nHow would you like to sort the data in the dataframe? "
                        "Press Enter to view unsorted.\n"
                        " [st] Start Time\n [et] End Time\n "
                        "[td] Trip Duration\n [ss] Start Station\n "
                        "[es] End Station\n\n>").lower()
            if sort_df in ['st', 'et', 'td', 'ss', 'es']:
                asc_or_desc = input("\nWould you like it to be sorted ascending or "
                                    "descending? \n [a] Ascending\n [d] Descending\n\n>").lower()
                ascending = True if asc_or_desc == 'a' else False
                if sort_df == 'st':
                    df = df.sort_values('Start Time', ascending=ascending)        
                elif sort_df == 'et':
                    df = df.sort_values('End Time', ascending=ascending)        
                elif sort_df == 'td':
                    df = df.sort_values('Trip Duration', ascending=ascending)        
                elif sort_df == 'ss':
                    df = df.sort_values('Start Station', ascending=ascending)        
                elif sort_df == 'es':
                    df = df.sort_values('End Station', ascending=ascending)        
                break
            
    # Display 5 lines of raw data at a time
    while True:
        print("\n")
        print(df.iloc[mark_place:mark_place + 5].to_string(index=False))
        print("\n")
        mark_place += 5

        choice_input = input("Do you want to keep printing raw data?"
                             "\n\n[y] Yes\n[n] No\n\n>").lower()
        if choice_input != 'y':
            break

    return mark_place



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        mark_place = 0
        while True:
            select_data = input("\nPlease select:\n\n"
            					"[ts] Time Stats\n"
                                "[ss] Station Stats\n"
                                "[tds] Trip Duration Stats\n"
                                "[us] User Stats\n"
                                "[rd] Display Raw Data\n"
                                "[r] Restart\n\n>").lower()
            if select_data == 'ts':
                time_stats(df)
            elif select_data == 'ss':
                station_stats(df)
            elif select_data == 'tds':
                trip_duration_stats(df)
            elif select_data == 'us':
                user_stats(df, city)
            elif select_data == 'rd':
                mark_place = raw_data(df, mark_place)
            elif select_data == 'r':
                break

        restart = input("\nWould you like to restart?\n\n[y] Yes\n[n] No\n\n>").lower()
        if restart != 'y':
            break


if __name__ == "__main__":
    main()
