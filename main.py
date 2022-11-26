import settings
import discord
from discord import app_commands
from discord.ext import commands

logger = settings.logging.getLogger("bot")

def returnRoles(interaction: discord.Interaction):
    overlap = []
    count = 0
    for member in interaction[0].members:
        for role in member.roles:
            for r in interaction:
                if role.name == r.name:
                    count+=1
        if count == len(interaction):
            overlap.append(member)
        count = 0
    return overlap

def run():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    bot = commands.Bot(command_prefix="!", intents=intents)
    
    @bot.event
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")
        print("_______________")
        # sync comands
        try:
            synced = await bot.tree.sync()
            print(f"Synced {len(synced)} command")
        except Exception as e:
            print(e)

    @bot.event
    async def on_command_error(interaction, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await interaction.send("Error occured.")

    @bot.command(
        aliases=['i','inv'],
        help="Create invite link for this bot",
        description="Generates an invite link for this bot",
        brief="Create invite link",
        enabled=True,
        hidden=False
    )
    async def invite(interaction: discord.Interaction):
        await interaction.send("https://discord.com/api/oauth2/authorize?client_id=1045768782074892381&permissions=274877908992&scope=bot%20applications.commands")

    @bot.tree.command(name="list_members_with_roles")
    @app_commands.describe(role1="List all members with up to 3 overlapping roles")
    async def listRoles(interaction: discord.Interaction, role1: discord.Role,
    role2: discord.Role = None, role3: discord.Role = None, nickname: bool = True
    ):
        def getName(m : discord.Member):
            if nickname and m.nick != None:
                name = m.nick
            elif nickname and m.nick == None:
                name = m.name
            else:
                name= m.name+"#"+m.discriminator
            return name

        name = getName(interaction.user)
        list = [role1,role2,role3]
        for l in list[:]:
            if l == None:
                list.remove(l)
        listOfMembers = returnRoles(list)
        roleTuple = tuple(i.name for i in list)
        memberLength = len(listOfMembers)
        if  len(roleTuple) > 1:
            howMany = "overlap with the roles"
        else:
            howMany = "have the role"
        initialRequest = "`{}` requested list of members that {} of `@{}`\n".format(name,howMany,"` & `@".join(roleTuple))

        if memberLength == 0:
            results = ("```No results were found. Please try broadening your search.```",)
        else:
            count = 1
            results = ("```",)
            for m in listOfMembers:
                results = results + ((str(count) +". " + getName(m)),)
                count+= 1
            results = results + ("```",)
        post = "{}{}".format(initialRequest, "\n".join(results))
        logger.info(post)
        await interaction.response.send_message(post)


    bot.run(settings.DISCORD_API_SECRET, root_logger=True)

if __name__ == "__main__":
    run()