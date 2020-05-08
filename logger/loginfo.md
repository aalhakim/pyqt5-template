## Purpose

The purpose of the logs (especially where we are all remote now) is to allow us to debug if there are problems. We want to know:

- What exactly happened?
- When exactly did it happen?
- What exactly was the status of the application when it happened?
- What exactly did the user do to make it happen?

## Logging Levels

Use at least 4 different logging levels to support different severity levels of events:

- Debug
- Info
- Warning
- Error

### Debug Level

Generally uninteresting stuff but provides some insight into where the application is at a given time. This information should only be written to a file (e.g. debug.log) and not displayed in the console e.g

``` console
>> DEBUG: '<serial_number>' - Received serial number
>> DEBUG: '<serial_number>' - Starting validation
```

### Info Level

A bit more interesting to be informed of. This should be displayed in a terminal/console window so that there is visibility that this has happened. These logs should also be written to the debug.log file, but also to it's own file info.log e.g.

``` console
>> INFO: 'serial number' - Validation successful.
```

### Warning Level

A relatively serious issue which is not critical (i.e. won't stop operation of the application) but the user should be clearly warned about. These should be written to all both lower level log files (debug.log, info.log) but a new unique log is not required.

``` console
>> WARNING: 'serial number' - Unexpected format - could not proceed
>> WARNING: Printer not found
```

### Error Level

A serious issue will may cause the application to crash or not work properly. It therefore needs to be clearly highlighted. You may insert these for example if catch all 'else' statements which you hope to never fall into but maybe one day you will. These should be written to all lower level log files (debug.log, info.log) and a new top level file error.log.

``` console
>> ERROR: Index Error - list cannot be index by '<index_value>'.
```

## Log File Management

Logs should be displayed in the console window (for Info level and above) and written to file as below:

### Files

| Log Level | debug.log | info.log | error.log
| :-------- | :-------: | :------: | :-------:
| Debug     | ✔ |   |
| Info      | ✔ | ✔ |
| Warning   | ✔ | ✔ |
| Error     | ✔ | ✔ | ✔

### Size Management

Log files should not be allowed to infinitely grow so one of the following systems should be implemented:

Generate a new set of logs per day. Expire (delete) all logs that are a week old.

Implement a rotating log structure so that all log files can only reach a certain size (e.g. 5 MB) before a new log file is opened or start overwriting the current log.
