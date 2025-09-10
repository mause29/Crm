import sys, json
from ai_chatbot import generate_response

args = json.loads(sys.argv[1])
clientMessage = args.get("clientMessage")
clientId = args.get("clientId")

reply = generate_response(clientMessage, clientId)
print(json.dumps({"reply": reply}))
