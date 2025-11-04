'''
Custom authentication checks.
'''

## django
from django.core.exceptions import ValidationError as DjangoValidationError 

def get_token_user_groups(request) -> list :
    '''
    Gets the groups that this user is part of from the token
    Arguments:
        request -- GET/POST/PUT request
    Returns:
        list (string) -- a list of strings representing the user groups
    '''
    if request is None or request.auth is None:
        return []
    token_payload_groups = request.auth.get('groups',[])  
    # permissions = token_payload.get('permissions', [])
    return token_payload_groups



def request_auth_has_group(request, group_names: list) -> bool: 
    '''
    Checks if the request.auth contains one of the group_names.
    Arguments:
        request -- GET/POST/PUT request
        group_names -- list of strings representing the group names.
    Returns:
        bool -- 
    '''
    token_payload_groups = get_token_user_groups(request=request)

    for group_name in group_names:
        if group_name in token_payload_groups:
            return True
    
    return False



def get_token_userid(request) -> int | None:
    '''
    Gets the user id from the token
    Arguments:
        request -- GET/POST/PUT request
    Returns:
        int -- user id if it was found
        None --- no user id was found
    '''
    if request is None or request.auth is None:
        return None
    return request.auth.get('user_id',None)  



def get_request_file(request, MAX_FILE_UPLOAD_SIZE_MB: int=25):
    """
    Returns the uploaded file 
    Raises:
        ValidationError -- on file missing, not ending with '.csv', exceeding max size
    """
    uploaded_file = request.FILES.get('file')
    if uploaded_file is None:
        raise DjangoValidationError({"file":["Missing file"]})
    
    ## Check file name extension
    if not uploaded_file.name.endswith('.csv'):
        raise DjangoValidationError({"file":["Uploaded file is not a CSV."]})
        
    ## Check file size
    max_size = MAX_FILE_UPLOAD_SIZE_MB * 1024 * 1024  ## in bytes
    if uploaded_file.size > max_size:
        raise DjangoValidationError({"file":[f'File size exceeds {MAX_FILE_UPLOAD_SIZE_MB}MB limit.']})

    return uploaded_file