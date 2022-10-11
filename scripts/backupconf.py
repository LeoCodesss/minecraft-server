#all timezones: https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568
timezone="Europe/Berlin"

#backuped file name
#"[FILENAME]" will be replaced with the name of the backuped file
#%a: Returns the first three characters of the weekday, e.g. Wed.
#%A: Returns the full name of the weekday, e.g. Wednesday.
#%B: Returns the full name of the month, e.g. September.
#%w: Returns the weekday as a number, from 0 to 6, with Sunday being 0.
#%m: Returns the month as a number, from 01 to 12.
#%p: Returns AM/PM for time.
#%y: Returns the year in two-digit format, that is, without the century. For example, "18" instead of "2018".
#%Y: Returns the year in four-digit format, that is, with the century. For example, "2018" instead of "18".
#%f: Returns microsecond from 000000 to 999999.
#%Z: Returns the timezone.
#%z: Returns UTC offset.
#%j: Returns the number of the day in the year, from 001 to 366.
#%W: Returns the week number of the year, from 00 to 53, with Monday being counted as the first day of the week.
#%U: Returns the week number of the year, from 00 to 53, with Sunday counted as the first day of each week.
#%c: Returns the local date and time version.
#%x: Returns the local version of date.
#+%X: Returns the local version of time.
filename="[FILENAME] %d.%m.%Y %H:%M"

#when to make a backup
#"dynamic" for minutes or hours, "static" for a specific time like 16:30
backuptimeformat="dynamic"
#m for minutes and h for hours, if you are using "static" you can add mulitple times divided by a space
backuptime="1m"

#smart bakups
#when set to true it will only backup if a player is on the server
smartbackups=True