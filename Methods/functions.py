def process_date(user_datetime, player):
    from datetime import datetime, timedelta
    import pytz
    from babel.dates import format_date

    # Pre-define constants
    KYIV_TZ = pytz.timezone('Europe/Kyiv')

    if user_datetime == 'Игрок не найден':
        return user_datetime 

    # Get the current time in Kyiv timezone
    kyiv_date = datetime.now(KYIV_TZ).date()

    # Parse and adjust the datetime in one step
    adjusted_datetime = datetime.strptime(user_datetime[:16], "%Y-%m-%dT%H:%M") + timedelta(hours=3)

    parsed_time = adjusted_datetime.strftime("%H:%M")
    parsed_date = adjusted_datetime.date()

    # Compare dates
    date_diff = (kyiv_date - parsed_date).days
    if date_diff == 0:
        formatted_date = "сегодня"
    elif date_diff == 1:
        formatted_date = "вчера"
    else:
        formatted_date = format_date(parsed_date, format="d MMMM", locale='ru')

    # Creating a message to be sent by bot
    return f"Игрок {player} был в сети в {parsed_time}, {formatted_date}"