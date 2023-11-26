import logging
import azure.functions as func
from main import main

app = func.FunctionApp()


@app.function_name("CronMail")
@app.schedule(
    schedule="0 30 14 * * *",
    arg_name="myTimer",
    run_on_startup=False,
    use_monitor=False,
)
def daily_mail(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info("The timer is past due!")
    main()
    logging.info("Python timer trigger function executed.")


@app.function_name("HttpMail")
@app.route(route="send", auth_level=func.AuthLevel.ANONYMOUS)
def http_mail(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Running HTTP Trigger")
    main()
    return func.HttpResponse("HTTP trigger executed successfully.", status_code=200)
