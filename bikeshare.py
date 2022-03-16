#import section
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
#Subroutine getting user's inputs
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
        CITIES= ['chicago','new york city','washington']
        print("\nEnter the full name of city you would like to analyse : (Chicago, New york city, Washington)")
        print("not case sensitive (e.g. washington or WASHINGTON)\n")
        CITY= input(" --> ").lower()
        if CITY in CITIES:
            CITY=CITY.lower()
            print('-'*40)
            break
        else:
            print("\n><-----------------------><")
            print("><--city name not valid--><") 
            print("><-----------------------><")   
# get user input for month (all, january, february, ... , june)
    while True:
        MONTHS= ['january','february','march','april','may','june','all']
        print("\n Let\'s enter the month you would like to analyse : (January, February, March, April, May, June) or all")
        print("not case sensitive (e.g. january or JANUARY)")
        MONTH = input("\n --> ").lower()
        if MONTH in MONTHS:
            print('-'*80)
            break
        else:
            print("\n><-----------------------><")
            print("><----month not valid----><") 
            print("><-----------------------><") 
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        DAYS= ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']
        print("\n Let\'s enter the day of the week you would like to analyse? (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday) or all")    
        print("not case sensitive (e.g. monday or MONDAY)")
        DAY = input("\n --> ").lower()
        if DAY in DAYS:
            print('-'*80)
            break
        else:
            print("\n><---------------------><")
            print("><----day not valid----><") 
            print("><---------------------><")    

    print('Filter settings --> CITY= {} ,MONTH= {} ,DAY= {}'.format(CITY.title(), MONTH.title(), DAY.title()))
    print('_'*80)
    return CITY, MONTH, DAY
#--------------------------------------------------------------------------------------------------------
#Subroutine loading the data
def load_data(CITY, MONTH, DAY):
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
    df = pd.read_csv(CITY_DATA[CITY])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['Month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_of_week
    
    # filter by month when a month is selected
    if MONTH != 'all':
        # use the index of the months list to get the corresponding int
        MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']
        MONTH = MONTHS.index(MONTH) + 1 #first month starts with 1 (January)
    
        # filter by month to create the new dataframe
        df = df[df['Month'] == MONTH]

    # filter by day of week when a day is selected
    if DAY != 'all':
        DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday','sunday']
        DAY = DAYS.index(DAY) + 0 #first day of the week starts with 0 (Monday)
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == DAY]
    return df
#-------------------------------------------------------------------------------------------------
#Subroutine calculating time statistics
def time_stats(df,MONTH,DAY):
    """Displays statistics on the most frequent times of travel."""

    print('Calculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month (only when all month selected)
    if MONTH =='all':
        most_common_month= df['Month'].mode()[0]
        MONTHS= ['January','February','March','April','May','June']
        most_common_month= MONTHS[most_common_month-1]
        print("The most Popular month is : ",most_common_month)   
        print('-'*80)
    
    # display the most common day of week (only when all days selected)
    if DAY =='all':
        MOST_COMMON_DAY= df['day_of_week'].mode()[0]
        DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']
        MOST_COMMON_DAY=DAYS[MOST_COMMON_DAY-1]
        print("The most Popular day is",MOST_COMMON_DAY)
        print("This took %s seconds." % (time.time() - start_time))
        print('-'*80)

    # display the most common start hour
    # before we need to extract hour from the Start Time column to create an hour column
    df['Start Hour'] =df['Start Time'].dt.hour
    MOST_COMMON_HOUR=df['Start Hour'].mode()[0]
    print('The most Frequent Start Hour: {} h'.format(MOST_COMMON_HOUR))
    print("This took %s seconds." % (time.time() - start_time))
    print('-'*80)
#----------------------------------------------------------------------------------------------------    
#Subroutine calculating stations stats  
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('Calculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
   MOST_COMMON_START_STATION= df['Start Station'].mode()[0]
    print("The most popular Start Station is {}".format(MOST_COMMON_START_STATION))

    # display most commonly used end station
    MOST_COMMON_END_STATION= df['End Station'].mode()[0]
    print("The most popular end Station is {}".format(MOST_COMMON_END_STATION))

    # display most frequent combination of start station and end station trip
    # create combination of start station and end station trip column first
    df['Start_End_Station']=df['Start Station']+"-->"+ df['End Station']
    MOST_POPULAR_STARTEND_STATION= df['Start_End_Station'].mode()[0]
    print("The most frequent combination of Start and End Station is {} ".format(MOST_POPULAR_STARTEND_STATION))

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
#Subroutine calculating trip duration stats
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('Calculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    TOTAL_TRIP_DURATION=df['Trip Duration'].sum()
    print("The total travel time in seconds :",TOTAL_TRIP_DURATION)
    print("The total travel time : {} ".format(convert(TOTAL_TRIP_DURATION)))

    # display mean travel time
    MEAN_TRAVEL_TIME=df['Trip Duration'].mean()
    print("The mean travel time in seconds : ",MEAN_TRAVEL_TIME)
    print("The mean travel time : ",convert(MEAN_TRAVEL_TIME))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)
#----------------------------------------------------------------------------------------------------      
def user_stats(df,CITY):
    """Displays statistics on bikeshare users."""

    print('Calculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    COUNT_USER_TYPE= df['User Type'].value_counts()
    print("counts of user types : ",COUNT_USER_TYPEe)

    # Display counts of gender / valid only for Chicago and NYC
    if CITY == 'chicago' or CITY == 'new york city':
        COUNT_GENDER= df['Gender'].value_counts()
        print("counts of gender :",COUNT_GENDER)
      
    # Display earliest, most recent, and most common year of birth
        EARLIEST_BIRTH= int(df['Birth Year'].min())
        print("date of birth of the oldest end-user ",EARLIEST_BIRTH)
        MOST_RECENT_BIRTH= int(df['Birth Year'].max())
        print("date of birth of the youngest end-user",MOST_RECENT_BIRTH)
        MOST_COMMON_BIRTH= int(df['Birth Year'].mode()[0])
        print("Most users are born of the year",MOST_COMMON_BIRTH)
    else :print("gender info not available for this city")    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)
#----------------------------------------------------------------------------------------------------        
#Raw data displayed upon request by the user (5 row at a time)
def Raw_data_display(df):
    START_ROW = 0
    END_ROW = 5
    LAST_ROW = df.shape[0]
    print('\nTotal number of row in the raw data selected : ',LAST_ROW)

    print("Wana have a look into raw data (5 rows)? : 'y' or any other key to exit\n")
    USER_INPUT_1st= input("  -->  ").lower()
    if USER_INPUT_1st=='y':
        print((df[START_ROW:END_ROW]).to_string(index=False))
        #while True: #using while loop and track the row index in order to display the continuous raw data
        while True and END_ROW <= LAST_ROW:
         print("Wanna see 5 more rows? : 'y' or any other key to exit")   
         USER_INPUT_n= input("  -->  ").lower()   
         if USER_INPUT_n=='y':
            # Deletes the question after "yes" input to make a more readable list
            print("\033[A                             \033[A")
            START_ROW += 5
            END_ROW += 5
            if END_ROW <= LAST_ROW:
              # Deletes the question after "yes" input to make a more readable list   
              print("\033[A                             \033[A")  
              print((df[START_ROW:END_ROW]).to_string(index=False, header=False))
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
        CITY, MONTH, DAY = get_filters()
        df = load_data(CITY, MONTH, DAY)

        time_stats(df,MONTH,DAY)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,CITY)
        Raw_data_display(df)

        restart = input('Would you like to restart? Enter yes or no --> ')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()    
exit()