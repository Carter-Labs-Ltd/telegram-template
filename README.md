# telegram-template

In a previous version of our API we supported native Telegram and Discord integration. This was pretty popular but had a few issues:

- Couldn't be customised by Carter developers.
- Didn't scale very well for larger user bases.
- Didn't support cool features like voice messages etc.

We've decided that the core focus of the API should be the interactions itself, integrations with the API should be separate projects that can be managed by developers to give much more granular control.

For those reasons, here's an Open Source template that brings the new API to Telegram due to popular demand. Currently it supports only text, but as we all know, Carter uses voice too so potentially open sourcing this part of the system will lead to greater improvement down the line for everyone.

You can find the template on here as well as a Repl that can be deployed with the click of a button.

Replit:
https://replit.com/@HuwProsser/CarterTelegramBotDemo?v=1
