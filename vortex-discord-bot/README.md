# Vortex Discord Bot

A 24/7 assistant for the Vortex Realm Discord: AI help (OpenRouter free models), tickets with transcripts, polls, giveaways and
competitions, tournaments with brackets, self-roles, staff role changes, welcome messages and announcements.

## Run it
1. Discord Developer Portal → your app → **Bot** → turn on **Server Members Intent** and **Message Content Intent**.
2. Copy `.env.example` to `.env` and fill in a **new** bot token and your OpenRouter key (`AI_API_KEY`, starts with sk-or-).
3. `npm install` then `npm start` (Node 18 or newer). Keep it running on a host that is always on.

## Commands
| Command | Who | What |
|---|---|---|
| `/ask` | everyone | ask the assistant (it also answers when mentioned, in #questions, #bot-commands and in tickets) |
| `/ip` | everyone | how to join |
| `/poll` | everyone | poll with buttons and live results |
| `/tournament bracket` | everyone | show the bracket |
| `/ticket-panel` | staff | post the ticket buttons (Support, Report, Appeal, Store) |
| `/roles-panel` | staff | post region and PvP/SMP self-roles |
| `/giveaway` | staff | giveaway or competition with an Enter button; winners picked automatically |
| `/tournament create / start / win` | staff | sign-ups, random bracket, report winners until a champion |
| `/rank give/remove` | staff | change a member's role (logged in #staff-actions) |
| `/announce` | staff | embed announcement, optional @everyone |
