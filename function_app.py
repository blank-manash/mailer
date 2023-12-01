import azure.functions as func
from main import main
from flow_chart import flow_reponse
from config import get_logger
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
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, PUT, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
    }

    # Handle preflight OPTIONS request
    if req.method == "OPTIONS":
        # OPTIONS requests may require additional headers
        return func.HttpResponse(status_code=204, headers=headers)
    try:
        text = req.get_json()["text"]
        flow_json = flow_reponse(text)
        response = json.dumps(flow_json)
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
