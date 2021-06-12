

@disable_if_update_coming
@limit_one_game_per_person
async def glolfcommand(message):
    # parse a glolf command

    arguments = message.content.split("\n") #first line has "!glolf" on it
    glolfer_names = []
    if len(arguments) > 1: # 0 players is fine
        glolfer_names = arguments[1:]
        if len(glolfer_names) == 1:
            await message.channel.send("It's too dangerous to glolf alone. Bring an opponent.")
            return

    if len(users_with_games_active) > MAX_GAMES:
        await message.channel.send("There's too many games going on right now. To avoid lag, please wait a little bit till some games are done and try again later!")
        return
        

    await newglolfgame(message, glolfer_names)

async def newglolfgame(message, glolfer_names, header=None, max_turns=60, is_tournament=False):
    # start a round of glolf and return the winning players's names

    glolfgame = await message.channel.send("Beginning game...")
    logging.info(f"Starting game between {glolfer_names} in channel #{message.channel} in server '{message.channel.guild.name}'")
    try:
        game = SingleHole(debug=debug,glolfer_names=glolfer_names,max_turns=max_turns,is_tournament=is_tournament)
        await asyncio.sleep(2)
        await glolfgame.edit(content=game.printgamestate(header=header))
        await asyncio.sleep(2)

        while not game.over:
            delay = game.update()
            await glolfgame.edit(content=game.printgamestate(header=header))
            await asyncio.sleep(delay)

        await glolfgame.edit(content=game.printgamestate(include_board=True,header=header))
        await asyncio.sleep(10)
        await glolfgame.edit(content=game.printgamestate(include_board=False,header=header))
        return game.compute_winners()
    except (Exception, KeyboardInterrupt) as e:
            await glolfgame.add_reaction('⚠️')
            raise e
