import azure.functions as func
from main import main
from flow_chart import flow_reponse
from config import get_logger, get_headers, get_chat_client, GPTModels
import json

logger = get_logger()
app = func.FunctionApp()


@app.function_name("CronMail")
@app.schedule(
    schedule="0 30 7 * * *",
    arg_name="myTimer",
    run_on_startup=False,
    use_monitor=True,
)
def daily_mail(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logger.info("The timer is past due!")
    main()
    logger.info("Python timer trigger function executed.")


@app.function_name("HttpMail")
@app.route(route="send", auth_level=func.AuthLevel.ANONYMOUS)
def http_mail(req: func.HttpRequest) -> func.HttpResponse:
    logger.info("Running HTTP Trigger")
    main()
    return func.HttpResponse(
        "HTTP trigger executed successfully.", status_code=200
    )


@app.function_name("CreateFlowChart")
@app.route(route="create-flow", auth_level=func.AuthLevel.ANONYMOUS)
def create_flow(req: func.HttpRequest) -> func.HttpResponse:
    logger.info("Creating Flow")
    headers = get_headers()
    if req.method == "OPTIONS":
        return func.HttpResponse(status_code=204, headers=headers)
    try:
        text = req.get_json()["text"]
        response = flow_reponse(text)
        response = json.dumps(response)
        return func.HttpResponse(response, status_code=200, headers=headers)
    except Exception as e:
        return func.HttpResponse(
            json.dumps(
                {
                    "data": f"Error in Receiving Data: {str(e)}",
                    "success": False,
                }
            ),
            status_code=400,
            headers=headers,
        )


@app.function_name("Suggestions")
@app.route(route="suggestions", auth_level=func.AuthLevel.ANONYMOUS)
def suggest(req: func.HttpRequest) -> func.HttpResponse:
    logger.info("Suggestions")
    headers = get_headers()
    if req.method == "OPTIONS":
        return func.HttpResponse(status_code=204, headers=headers)
    try:
        text = req.get_json()["text"]
        prompt = f"""Create a autocomplete suggestion based on this text:
        {text}

        Your response should only be the suggestion. It will be directly fed to user.
        DO NOT Write anything else. Create a Completion under 100 words.
        """.replace(text=text)
        gpt = get_chat_client(GPTModels.GPT4)
        response = {"suggestion": gpt(prompt=prompt)}
        response = json.dumps(response)
        return func.HttpResponse(response, status_code=200, headers=headers)
    except Exception as e:
        return func.HttpResponse(
            json.dumps(
                {
                    "data": f"Error in Receiving Data: {str(e)}",
                    "success": False,
                }
            ),
            status_code=400,
            headers=headers,
        )
