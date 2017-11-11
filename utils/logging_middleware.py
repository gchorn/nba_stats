""" Custom Middleware class for logging requests to the Django app """
import logging
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)


class LoggingMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response
        logger.info({
            'msg': 'App initialized'
        })

    def __call__(self, request):
        before_request = datetime.now()
        request_id = uuid.uuid4()

        response = self.get_response(request)

        request_time = datetime.now() - before_request

        try:
            view_info = response.renderer_context.get('view')
        except AttributeError:
            view_info = None

        logger.info({
            'msg': 'Django app request',
            'request_id': request_id,
            'request_url': request.build_absolute_uri(),
            'view': view_info.__class__,
            'method': request.method,
            'querystring': request.environ['QUERY_STRING'],
            'body': request.body.decode('utf-8') or None,
            'response_time_ms': (request_time.seconds * 1000) + (request_time.microseconds / 1000)
        })

        return response