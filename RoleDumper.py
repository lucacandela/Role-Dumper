import discord
import DiscordTokens

class RoleDumper:
    def createInviteLink(self):
        webLink = "https://discord.com/api/oauth2/authorize?client_id=" + DiscordTokens.client_ID + "&permissions=275146344512&scope=bot%20applications.commands"
        return webLink
