# -- coding: utf-8 --
import discum, requests, json, os, threading, time

config = json.loads(open("config.json", "r").read())

token = config["token"]
guild_id = config["guild_id"]
channel_id = config["channel_id"]

c = 0


def download_profile(id, avatar, username):
    global c
    open(f"Guilds/{guild_id}/Avatars/{id}.png", "wb").write(requests.get(f"https://cdn.discordapp.com/avatars/{id}/{avatar}.png?size=512").content)
    c += 1

bot = discum.Client(token=token, log=False)

def close_after_fetching(resp, guild_id):
    if bot.gateway.finishedMemberFetching(guild_id):
        len(bot.gateway.session.guild(guild_id).members)
        bot.gateway.removeCommand({'function': close_after_fetching, 'params': {'guild_id': guild_id}})
        bot.gateway.close()

def get_members(guild_id, channel_id):
    bot.gateway.fetchMembers(guild_id, channel_id, keep='all', wait=0)
    bot.gateway.command({'function': close_after_fetching, 'params': {'guild_id': guild_id}})
    bot.gateway.run()
    bot.gateway.resetSession()
    return bot.gateway.session.guild(guild_id).members


members = get_members(guild_id=guild_id, channel_id=channel_id)

info = [

]

try:
    os.makedirs(f"Guilds/{guild_id}")
except:
    pass
try:
    os.makedirs(f"Guilds/{guild_id}/Avatars")
except:
    pass
for member in members:
    user = members[str(member)]
    userinfo = {
        "id": member,
        "username": user["username"] + "#" + user["discriminator"],
        "avatar": user["avatar"]
    }
    info.append(userinfo)

ids = []
usernames = []
for member in info:
    ids.append(member["id"])
    print(member["id"] + "ㅣ" + member["username"])
    usernames.append(str(member["username"])[:len(member["username"])-5])
    if member["avatar"] != None:
        threading.Thread(target=download_profile, args=(member["id"], member["avatar"], member["username"],)).start()
    else:
        c+=1
open(f"Guilds/{guild_id}/Ids.txt", "w").write("\n".join(ids))
open(f"Guilds/{guild_id}/Usernames.txt", "w", encoding="utf-8").write("\n".join(usernames))
while True:
    if c == len(info):
        break

os.system("pause")
