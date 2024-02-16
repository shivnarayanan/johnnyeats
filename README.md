## Local Development

Follow these steps and set up your development environment:

1. To create a bot, use Telegram's special bot called BotFather. 
    1. Search for "@BotFather" in Telegram and start a chat. 
    2. Follow the instructions to create a new bot by typing **`/newbot`** and providing a name and username. 
    3. BotFather will provide you with a token to use for HTTP API access.
2. Clone GitHub Repository: `git clone https://github.com/shivnarayanan/johnnyeats.git`
3. Create a **.env** file within the project directory 
4. Add `BOT_TOKEN=XXX` to the file and replace `XXX` with the token from BotFather.
5. Create Conda Environment: `conda create --name johnnyeats`
6. Activate Conda Environment:`conda activate johnnyeats`
7. Install pip in Conda Environment: `conda install pip` 
8. Install required libraries: `pip install -r requirements.txt`
9. To test the bot on Telegram, run `python3 main.py` and search for your bot on Telegram.

## Food and Drinks Data

The bot retrieves data from a [Heroku Postgres](https://devcenter.heroku.com/articles/heroku-postgresql) database. 

The database is updated daily by the **update.py** script, which runs on [Heroku Scheduler](https://devcenter.heroku.com/articles/scheduler). It retrieves data from [here](https://docs.google.com/spreadsheets/d/10KDw1cMOw4NaSXAJS8QObgpUnsfbWdj72ERZagWjoEs/edit#gid=1593634417).

## Deployment

The development and production bots are deployed on Heroku. Automated deployment is triggered when changes are merged into the **develop** or **main** branches.

- Merging into the **develop** branch deploy changes into the **DEVJohnnyEats** development bot.
- Merging into the **main** branch deploys changes into the **JohnnyEats** production bot.

If you are interested in the deployment set-up, ask Shiv to add you as a collaborator to the application on Heroku.

## Task List

Click here to view the list of pending tasks.