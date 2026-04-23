"""Custom exception handler for standardized error responses."""
from rest_framework.views import exception_handler
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    """
    Custom exception handler that returns standardized error format.
    
    Format: {"error": "message", "code": "ERROR_CODE"}
    """
    response = exception_handler(exc, context)
    
    if response is not None:
        error_data = {
            'error': str(exc),
            'code': exc.__class__.__name__.upper()
        }
        
        if hasattr(exc, 'detail'):
            if isinstance(exc.detail, dict):
                error_data['error'] = exc.detail
            else:
                error_data['error'] = str(exc.detail)
        
        response.data = error_data
    
    return response
