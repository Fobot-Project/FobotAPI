from flask import Flask, request
from blueprints.basic_endpoints import blueprint as basic_endpoints
from blueprints.jinja_endpoint import blueprint as jinja_template_blueprint
from blueprints.documented_endpoints import blueprint as documented_endpoint
from firebase_admin import firestore
import json

app = Flask(__name__)
app.config['RESTPLUS_MASK_SWAGGER'] = False
db = firestore.client()
list1 = []
list1.append(0)
@app.route('/', methods=["POST","GET"])
def webhook():
    if request.method == 'GET':
        return 'Hello World.'
    elif request.method == 'POST':
        payload = request.json
        sessionID = (payload['session'].split("/")[-1])
        print(list1)
        print(list1[0])
        if list1[0] != sessionID:
            list1.clear()
            list1.append(sessionID)
        UserID = (payload['originalDetectIntentRequest']['payload']['userId'].split('/')[0])
        RestaurantID = (payload['originalDetectIntentRequest']['payload']['userId'].split('/')[1])
        intent = (payload['queryResult']['intent']['displayName'])
        # agentID = (payload['webhookStatus'])
        # print(agentID)
        # print(payload)
        print("sessionID:", sessionID)
        print("UserID:", UserID)
        print("RestaurantID:", RestaurantID)
        print("intent:", intent)

        user_response = (payload['queryResult']['queryText'])
        bot_response = (payload['queryResult']['fulfillmentMessages'])


        if intent == 'ask_menu':
            print(payload)
            print(bot_response)
            return{
                    "fulfillmentMessages":[{
                    "payload":{
                        "richContent":[[
                            {
                            "text":"Here is our menu.",
                             "type":"button",
                            "icon":{
                                "type": "link",
                                "color": "#FF9800"
                            },
                            "link":"https://firebasestorage.googleapis.com/v0/b/test-bot-hldq.appspot.com/o/users%20images%2Fv0cQnOfc7aJMHTbxSJIh%2Fmenu_images%2FMain_Menu.png?alt=media&token=44d883ab-80fd-4da2-8ccb-395289514779"
                        },
                            {
                                "type": "chips",
                                "options": [
                                    {
                                        "text": "Can I order now?"
                                    }]}
                                ]]
                    }
            }]
                }
        elif intent == 'order_now':

            print(payload)
            print(user_response)
            user_input = payload['queryResult']['parameters']
            print('user res:', user_response)
            list1.append(user_input)

            return 'ok'
        elif intent == "not_to_order":
            print(list1)
            list1.pop(-1)
            print(list1)
            return 'ok'

        elif intent == 'order_confirm':
            print('order_confirm:', list1)
            sessionid= list1[0]
            list1.pop(0)
            print('removed', list1)
            print('type', type(list1))
            res_ref = db.collection('User').document(UserID)
            newlist = res_ref.collection('Restaurants').document(RestaurantID).collection(u'Order').document(sessionid)
            print(list1[0])
            contact = payload['queryResult']['queryText']
            json_file = {'Contact':contact}
            for i in range(0,len(list1)):
                json_file[str(i)]=list1[i]

            print(json_file)
            print(type(json_file))
            newlist.set(
                 json_file

             )

            return 'ok'
        # elif intent == 'ask_recommendation':
        #     print(payload)
        #     print(bot_response)
        #     entity_list =[]
        #     user = db.collection('User').document(UserID)
        #     restaurants = user.collection('Restaurants').document(RestaurantID)
        #     menu = restaurants.collection('Menu').stream()
        #     for order in menu:
        #         Entity = order.to_dict()
        #         entity_list.append(Entity)
        #
        #     print(entity_list)
        #     print("[Sections]",entity_list['Sections'])
        #     return 'ok'

        else:
            return "something wrong"
        # if user_response or bot_response !='':
        #     print("User:", user_response)
        #     print("Bot:", bot_response)

    else:
        print(request.data)
        return '200'
app.register_blueprint(basic_endpoints)
app.register_blueprint(jinja_template_blueprint)
app.register_blueprint(documented_endpoint)

if __name__ == "__main__":
    app.run()