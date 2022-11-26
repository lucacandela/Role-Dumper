import settings
import discord
from discord import app_commands
from discord.ext import commands

logger = settings.logging.getLogger("bot")

def run():
    intents = discord.Intents.default()

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


    @bot.tree.command(name="list_members_with_role")
    @app_commands.describe(role="Role")
    async def listRoles(interaction: discord.Interaction, role: discord.Role):
        await interaction.response.send_message(f"{interaction.user.nick} requested list of members with '{role}'")

    bot.run(settings.DISCORD_API_SECRET, root_logger=True)

if __name__ == "__main__":
    run()