import uvicorn
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from src.bot import AgataBotGPT, Conversation

app = Starlette(debug=False)
response_header = { 'Access-Control-Allow-Origin': '*' }

agata = AgataBotGPT()
conversations = {}

def conversation_exists(id):
    for conv in conversations:
        if conv == id:
            return True, conversations[conv]
    return False, Conversation()

@app.route('/', methods=['GET', 'POST', 'HEAD'])
async def home_route(request):
    return JSONResponse(content={
        'message': 'Welcome to AgataBot GPT-2 API.',
        'info': 'This API only will run from 0.0.0.0 and is for local use only.',
        'developer': 'Cristian Valero Abundio'
    }, headers=response_header)

@app.route('/agata/answer/', methods=['POST'])
async def generate_answer(request):
    if request.method == 'POST':
        try:
            request_data = await request.json() #{'id': 3, 'question': ''}
            id, question = str(request_data['id']), str(request_data['question'])
            _, conv = conversation_exists(id)
            conv.append_context(question)
            answer = agata.interact_model(question=conv.context)
            conv.append_context(answer)
            conversations[id] = conv
            return JSONResponse(content={
                'id': str(id),
                'question': str(question),
                'answer': str(answer)
            }, headers=response_header)
        except:
            return JSONResponse(content={'error:': 'Request not valid.'}, headers=response_header)

@app.exception_handler(404)
def route_not_found(request, exc):
    return JSONResponse(content={
        'code': 404,
        'message': 'The route you requested not found. Please, try again or contact with an administrator.'
    }, status_code=exc.status_code)

if __name__ == '__main__':
    uvicorn.run(app, port=3001, host='0.0.0.0')
