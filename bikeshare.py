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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        cities= ['chicago','new york city','washington']
        print("\nEnter the full name of city you would like to analyse : (Chicago, New york city, Washington)")
        print("not case sensitive (e.g. washington or WASHINGTON)\n")
        city= input(" --> ").lower()
        if city in cities:
            city=city.lower()
            print('-'*40)
            break
        else:
            print("\n><-----------------------><")
            print("><--city name not valid--><") 
            print("><-----------------------><")   
# get user input for month (all, january, february, ... , june)
    while True:
        months= ['january','february','march','april','may','june','all']
        print("\n Let\'s enter the month you would like to analyse : (January, February, March, April, May, June) or all")
        print("not case sensitive (e.g. january or JANUARY)")
        month = input("\n --> ").lower()
        if month in months:
            print('-'*80)
            break
        else:
            print("\n><-----------------------><")
            print("><----month not valid----><") 
            print("><-----------------------><") 
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        days= ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']
        print("\n Let\'s enter the day of the week you would like to analyse? (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday) or all")    
        print("not case sensitive (e.g. monday or MONDAY)")
        day = input("\n --> ").lower()
        if day in days:
            print('-'*80)
            break
        else:
            print("\n><---------------------><")
            print("><----day not valid----><") 
            print("><---------------------><")    

    print('Filter settings --> CITY= {} ,MONTH= {} ,DAY= {}'.format(city.title(), month.title(), day.title()))
    print('_'*80)
    return city, month, day
#--------------------------------------------------------------------------------------------------------
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
    #Loading the file into a df
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_of_week
    
    # filter by month when a month is selected
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1 #first month starts with 1 (January)
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week when a day is selected
    if day != 'all':
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday','sunday']
        day = days.index(day) + 0 #first day of the week starts with 0 (Monday)
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]
    return df
#-------------------------------------------------------------------------------------------------
def time_stats(df,month,day):
    """Displays statistics on the most frequent times of travel."""

    print('Calculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month (only when all month selected)
    if month =='all':
        most_common_month= df['month'].mode()[0]
        months= ['January','February','March','April','May','June']
        most_common_month= months[most_common_month-1]
        print("The most Popular month is : ",most_common_month)   
        print('-'*80)
    
    # display the most common day of week (only when all days selected)
    if day =='all':
        most_common_day= df['day_of_week'].mode()[0]
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']
        most_common_day=days[most_common_day-1]
        print("The most Popular day is",most_common_day)
        print("This took %s seconds." % (time.time() - start_time))
        print('-'*80)

    # display the most common start hour
    # before we need to extract hour from the Start Time column to create an hour column
    df['Start Hour'] =df['Start Time'].dt.hour
    most_common_hour=df['Start Hour'].mode()[0]
    print('The most Frequent Start Hour: {} h'.format(most_common_hour))
    print("This took %s seconds." % (time.time() - start_time))
    print('-'*80)
#----------------------------------------------------------------------------------------------------    
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('Calculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station= df['Start Station'].mode()[0]
    print("The most popular Start Station is {}".format(most_common_start_station))

    # display most commonly used end station
    most_common_end_station= df['End Station'].mode()[0]
    print("The most popular end Station is {}".format(most_common_end_station))

    # display most frequent combination of start station and end station trip
    # create combination of start station and end station trip column first
    df['Start_End_Station']=df['Start Station']+"-->"+ df['End Station']
    most_popular_StartEnd_Station= df['Start_End_Station'].mode()[0]
    print("The most frequent combination of Start and End Station is {} ".format(most_popular_StartEnd_Station))

    print("This took %s seconds." % (time.time() - start_time))
    print('-'*80)
#----------------------------------------------------------------------------------------------------  
#routine to convert seconds in days, hours, minutes and seconds 
def convert(seconds):
    day = seconds // (24 * 3600)
    seconds = seconds % (24*3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
      
    return "d:h:m:s-> %d:%d:%d:%d" % (day, hour, minutes, seconds)    
#----------------------------------------------------------------------------------------------------   
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('Calculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_trip_duration=df['Trip Duration'].sum()
    print("The total travel time in seconds :",total_trip_duration)
    print("The total travel time : {} ".format(convert(total_trip_duration)))

    # display mean travel time
    mean_travel_time=df['Trip Duration'].mean()
    print("The mean travel time in seconds : ",mean_travel_time)
    print("The mean travel time : ",convert(mean_travel_time))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)
#----------------------------------------------------------------------------------------------------      
def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('Calculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_user_type= df['User Type'].value_counts()
    print("counts of user types : ",count_user_type)

    # Display counts of gender / valid only for Chicago and NYC
    if city == 'chicago' or city == 'new york city':
        count_gender= df['Gender'].value_counts()
        print("counts of gender :",count_gender)
      
    # Display earliest, most recent, and most common year of birth
        earliest_birth= int(df['Birth Year'].min())
        print("date of birth of the oldest end-user ",earliest_birth)
        most_recent_birth= int(df['Birth Year'].max())
        print("date of birth of the youngest end-user",most_recent_birth)
        most_common_birth= int(df['Birth Year'].mode()[0])
        print("Most users are born of the year",most_common_birth)
    else :print("gender info not available for this city")    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)
#----------------------------------------------------------------------------------------------------        
#Raw data displayed upon request by the user (5 row at a time)
def Raw_data_display(df):
    start_row = 0
    end_row = 5
    last_row = df.shape[0]
    print('\nTotal number of row in the raw data selected : ',last_row)

    print("Wana have a look into raw data (5 rows)? : 'y' or any other key to exit\n")
    user_input= input("  -->  ").lower()
    if user_input=='y':
        print((df[start_row:end_row]).to_string(index=False))
        #while True: #using while loop and track the row index in order to display the continuous raw data
        while True and end_row <= last_row:
         print("Wanna see 5 more rows? : 'y' or any other key to exit")   
         user_input2= input("  -->  ").lower()   
         if user_input2=='y':
            # Deletes the question after "yes" input to make a more readable list
            print("\033[A                             \033[A")
            start_row += 5
            end_row += 5
            if end_row <= last_row:
              # Deletes the question after "yes" input to make a more readable list   
              print("\033[A                             \033[A")  
              print((df[start_row:end_row]).to_string(index=False, header=False))
            else:
              print("\nEnd of List reached\n")
         else:
          print('-'*80)
          break 
    
#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------  
#Main program  
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df,month,day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        Raw_data_display(df)

        restart = input('Would you like to restart? Enter yes or no --> ')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()    
exit()