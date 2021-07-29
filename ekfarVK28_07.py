import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from pymongo import MongoClient

vk_session = vk_api.VkApi(os.environ['token'])
session_api = vk_session.get_api()
longpool = VkLongPoll(vk_session)

cluster = MongoClient(os.environ['mongo'])
bd = cluster["bd"]
collection = bd["vk"]

def send_some_msg(id, some_text):
    vk_session.method("messages.send", {"user_id":id, "message":some_text,"random_id":0})

for event in longpool.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            msg = event.text.lower()
            id = event.user_id
            send_some_msg(id,"Ваше сообещние доставлено в базу, дальше оно пойдет в дискорд экфару")

            count = collection.count_documents({})
            collection.insert_one({"id":id,'message':msg,"new":"yes",'super':id+count})

