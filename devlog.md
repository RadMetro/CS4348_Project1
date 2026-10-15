# 10-12-2026 9:17 pm
This is the first devlog, and today I simply set up the git.  
I set up the devlog file and the README.  
I have created the overview sections in the README.  
I have decided I'm going to start with the logger file.  
I have also decided that I will work on the project in Python.  
I'm not quite sure yet how the driver will communicate to the logger.  

# 10-13-2026 6:35 pm
I spent yesterday learning how to use Git which is why my day 1 devlog message is like that.  
The instructions/rubric said not to have commits that are one liners that don't explain the project but I didn't know how to use Git yet and so my day 1 commits ended up being one liners.

# 10-13-2026 7:10 pm
Today I plan to finish the logger and start on the encryption program. I'm still trying to figure out how the driver will work with the logger.
Especially how it will send it messages using pipes and subprocesses. 

# 10-13-2026 10:04 pm
I have finished creating the logger, but was unable to get to starting the encryption system.

The logger is a program that waits for input.
The driver sends the logger messages one line at a time, and adds a timestamp for each.
It does this until "QUIT" is sent.

**Implementation**
I read the input from sys.argv[1]. This is how I plan to have the driver tell which log file to use.
We read the input one line at a time.
We split off the first word and keep the rest of the line as the message.
We then check for QUIT, if the action is QUIT, the loop ends and we end the program. 
I make sure not to write QUIT to the log
*datetime.now().strftime("%Y-%m-%d %H:%M")* gives us the current date and 24 hour time.

I tested the logger by running the test input given as part of the assignment, and it gave the correct output.

**Problems**
I ran into some minor problems while working on the Logger.
I had a problem initially where typing QUIT would be written to the log as well then went ahead to correct that.
I had a problem where using split(" ") would cause breaks on multiple spaces.

**Next Session**
For the next session, I plan to implement the Encryption program.

# 10-14-2026 9:22 pm
Today I plan to write the encryption program.

The Encryption Program needs to read user input, one line at a time and print one line of reply for each.
Each line is a command followed by an argument. The first line is the command, and the rest of the line is the argument.

The driver will launch this program with subprocess, read back one line, and decide what to show the user and what to log.

The Vigenère cipher shifts the text based on a passkey.
If they key is shorter than the message it starts over.
It encrypts by adding each pair of numbers.

# 10-15-2026 2:28 AM
I finished the encryption program.

The program reads commands from standard input per line. 
It remembers the passkey between commands.
To encrypt, I used the vigenere function in my function. The vigenere function uses does the cipher as I described in my previous session.
Since encrypting adds a shift, decrypting simply removes it.

I tested the code by running python encryption.py

Some problems I had were forgetting to subtracting some stuff before shifting. 
And decrypting with the wrong sign.


For unknown commands, I reply with an ERROR unknown command message.
I have a reply() helper than helps print on one line and flushes every time. 

I'll next begin work on the Driver.


# 10-15-2026 4:38 pm
I'm starting work on the driver.
The driver will be the program that the user runs.
It will start the logger and the encryption program as child processes.
The driver will talk to the children through pipes, but won't encrypt or write itself.

Processes are isolated, so when I run a program, the OS creates a process with its own memory.
The driver, logger, and encryption program are there different processes, so they can't see each other's variables.
A pipe is the channel managed by the OS. Processes send messages to each other through pipes.

Before diving into the implementation, I need to make sure I understand how the driver will coordinate everything. 
Once set up, the driver needs to print a menu of commands, prompt the user, and loop until the quit command is received.
Every command and its result must be logged, and the start and exit of the driver itself also need to be recorded.

