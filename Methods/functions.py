#FUNCTION FOR DATE PROCESSING
def process_date(user_datetime, player):
    from datetime import datetime, timedelta

    if user_datetime == 'Игрок не найден':
        return user_datetime 


    import pytz
    from babel.dates import format_date
 
    # Accessing current date
    # Get the current time in UTC
    utc_now = datetime.now(pytz.utc)

    # Adjust to a different time zone, e.g., Europe/Moscow
    kyiv_tz = pytz.timezone('Europe/Kyiv')
    kyiv_date = utc_now.astimezone(kyiv_tz).date()

    # Processing received date time from API call

    date, time = user_datetime.split('T')
    time = time[:5]

    # Combine date and time into a single datetime object
    combined_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")

    # Adjust time by 3 hours
    adjusted_datetime = combined_datetime + timedelta(hours=3)

    # Get the adjusted time and date
    parsed_time = datetime.strftime(adjusted_datetime, "%H:%M")
    parsed_date = adjusted_datetime.date()  

    # Converts date to Russian language
    formatted_date = format_date(parsed_date, format="d MMMM", locale='ru')

    compare_result = compare_dates(kyiv_date, parsed_date)

    if  compare_result is not None:
        formatted_date = compare_result

    # Creating a message to be sent by bot
    message = f"Игрок {player} был в сети в {parsed_time}, {formatted_date}"

    return message

def compare_dates(date1, date2):
        from datetime import datetime, timedelta

        # Ensure both dates are datetime.date objects
        date1 = date1.date() if isinstance(date1, datetime) else date1
        date2 = date2.date() if isinstance(date2, datetime) else date2

        # Calculate the difference between the two dates
        difference = (date1 - date2).days

        # Compare the difference and print the appropriate message
        if difference == 0:
            result = "сегодня"  
        elif difference == 1:
            result = "вчера"
        else:
            return None

        return result
#END OF FUNCTION
