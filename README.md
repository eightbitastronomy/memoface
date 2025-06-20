# MemoFace
- wxPython frontend for MemoServ *** Under Construction ***
- Use with MemoServ, duh
## Usage
- make sure memoserv is running, preferrably as a background process
- start it up with the face.py script, i.e., e.g., python3 face.py
- Left-hand buttons are for switching between functions
- Once you've entered the info and made your choices, hit Apply/Go
## Requirements
- Mostly requires a version 4+ WxPython installation, haven't tested exactly what the minimum version is
- Requires packages json and dbus-python
## Caveats
- Again, is under construction
- In at least one instance (import call, maybe others in the future) I resorted to a call to busctl because I couldn't control the timeout value in the dbus-python library calls easily / in an obvious way. And I hit my own "timeout" on the amount of time and effort I was willing to spend on the problem.
- Some functionality appears in the frontend which does not in the backend, so I have tried to prevent these calls from being made wherever I noticed them
- Wanted the frontend to be fast, but am unsure I have accomplished that. It's meh on an AMD A8.
