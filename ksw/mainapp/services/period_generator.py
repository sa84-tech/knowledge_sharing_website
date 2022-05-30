import datetime
import dateutil.relativedelta
import calendar
import locale


def period_generator(request):
    today = datetime.date.today()
    periods = []
    locale.setlocale(locale.LC_ALL, '')
    for i in range(13):
        archive_data = today + dateutil.relativedelta.relativedelta(months=-i)
        archive_month = calendar.month_name[archive_data.month]

        title = archive_month + " " + str(archive_data.year)
        increment = {'name': title, 'archive_year': archive_data.year, 'archive_month': archive_data.month}
        periods.append(increment)

    return periods
