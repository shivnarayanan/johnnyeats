## Local Development

Follow these steps and set up your development environment:

1. Create a Telegram bot for local development:
    - Search for Telegram's special bot called @BotFather
    - Follow the instructions to create a new bot by typing **`/newbot`** and providing a name and username. 
    - BotFather will provide you with a token to use for HTTP API access.

2. Clone GitHub Repository: 
    ```
    git clone https://github.com/shivnarayanan/johnnyeats.git
    ```
3. Create a **.env** file within the project directory 
4. Add `BOT_TOKEN=XXX` to the file and replace `XXX` with the token from BotFather.
5. Prepare your enviornment:
    ```
    conda create --name johnnyeats
    conda activate johnnyeats
    conda install pip
    pip install -r requirements.txt
    ```
6. To test the bot, run `python3 main.py` and search for your bot on Telegram.

## Food and Drinks Data

The bot retrieves data from a [Heroku Postgres](https://devcenter.heroku.com/articles/heroku-postgresql) database. 

The database is updated daily by the **update.py** script, which runs on [Heroku Scheduler](https://devcenter.heroku.com/articles/scheduler). It retrieves data from [here](https://docs.google.com/spreadsheets/d/10KDw1cMOw4NaSXAJS8QObgpUnsfbWdj72ERZagWjoEs/edit#gid=1593634417).

## Deploymentgh

The staging and production bots are deployed on Heroku. Automated deployment is triggered when changes are merged into the **staging** or **main** branches.

- Merging into the **staging** branch deploy changes into the **STGJohnnyEats** staging bot.
- Merging into the **main** branch deploys changes into the **JohnnyEats** production bot.

If you are interested in the deployment set-up, ask Shiv to add you as a collaborator to the application on Heroku.

## Task List

Click here to view the list of pending tasks.