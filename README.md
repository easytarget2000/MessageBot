# Message Bot

A Python bot that randomly takes lines of text from a feed file. Currently only supports Twitter via Tweepy. Operates in non-repeating "regular" mode and in text-generating "poetry" mode.

### Regular Process flow: 
1. Lines are added to a feed file.
2. The feed file is copied and randomised into a temporary file.
3. Lines are read and posted from the temporary file.
4. Posted lines are deleted from the temporary file.
5. Once the temporary file is empty, go back to step 2.
