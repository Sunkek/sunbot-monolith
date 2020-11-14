# Sunbot

My discord bot. Rewritten. Again.

## Goals

- Collecting and displaying discord server and user statistics. 
- Automation of some boring stuff.
- Adding fun features to my discord community.
- Learning something new.

## Stack

- Python, obviously. The `discord.py` library is just awesome.
- For database I use PostgreSQL. 
- To address the database I use asyncpg for it's outstanding speed and just to practice my SQL.
- The bot and the database are used as Docker containers for easier deployment.

## Features & TODO

1. Settings - admins should be able to turn som,e options on and off and tune them
    - Set trackers
    - Set activity
    - Set emoji emotions
    - Set birthday feed
    - Set welcome and leave message
    - Set verification
    - Set ranks
    - Set special roles
    - Set warnings
2. Trackers - saving data to the database
    - ✔️ Message tracking
    - ✔️ Reaction tracking
    - ✔️ Voice tracking
    - ✔️ Games tracing
    - Emoji tracking
    - N-word tracking
    - Activity tracking
3. Topcharts - displaying saved data
    - Top postcounts
    - Top attachmetns
    - Top reactors
    - Top reaction receivers
    - Top voice chatters
    - Top players
    - Top channels, postcount
    - Top channels, attachments
    - Top channels, voice
    - Top emoji
    - Top games
    - Top countries
    - Top oldest
    - Top youngest
    - Top active members
4. Binder - collect some info about the members
    - Bind birthday
    - Bind steam
    - Bind country
5. Oracle - ask your questions
    - Just use the previously created one
6. Ad reminder - reminds you to bump your server
    - Just use the previously created one
7. Verification system - new members must prove that they're human
    - Send verified message
    - Purge unverified members daily, send message about it
8. Ranks - there's hierarchy everywhere
    - Automatically promote and demote members according to their activity and join date
    - Start votes for selected positions, send  message with candidate list
    - Send bulletins to those who can vote
    - Count the votes
    - Automaticlly promote and demote members according to the vote outcome
9. Special roles - personal titles
    - Let them create and change special roles if they meet the requirements
10. Mod functions - easier than Discord interface
    - Mute
    - Kick
    - Ban
11. Embedder - create and edit embed messages
    - New embed
    - Edit embed
    - Copy & paste embed
12. Russian roulette - feeling risky? 
    - Mute roulette
    - Kick roulette
    - Ban roulette
13. Warnings - easier automated moderation
    - Give warning
    - Automatically remove expired warnings
    - Take action according to the amount of active warnings
    
To be continued.
