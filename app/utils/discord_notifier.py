import aiohttp
from datetime import datetime

class DiscordNotifier:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    async def notify_script_update(self, script_name, version):
        embed = {
            "title": "🔄 Script Updated",
            "description": f"**Script:** {script_name}\n**Version:** {version}",
            "color": 0x9370DB,  # Crystal purple color
            "timestamp": datetime.utcnow().isoformat()
        }
        
        async with aiohttp.ClientSession() as session:
            await session.post(self.webhook_url, json={"embeds": [embed]})

    async def notify_purchase(self, user_id, script_name):
        embed = {
            "title": "💎 New Purchase",
            "description": f"**User:** <@{user_id}>\n**Script:** {script_name}",
            "color": 0x9370DB,
            "timestamp": datetime.utcnow().isoformat(),
            "fields": [
                {
                    "name": "Access",
                    "value": "✅ Granted automatically",
                    "inline": True
                },
                {
                    "name": "Support",
                    "value": "📞 24/7 Available",
                    "inline": True
                }
            ]
        }
        
        async with aiohttp.ClientSession() as session:
            await session.post(self.webhook_url, json={"embeds": [embed]})

    async def notify_hwid_reset(self, user_id):
        embed = {
            "title": "🔑 HWID Reset",
            "description": f"**User:** <@{user_id}>\n**Status:** Completed",
            "color": 0x9370DB,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        async with aiohttp.ClientSession() as session:
            await session.post(self.webhook_url, json={"embeds": [embed]})