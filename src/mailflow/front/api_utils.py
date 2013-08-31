from flask.ext.restless import ProcessingException


def _check_single_inbox(instance_id=None):
    print instance_id


def pre_get_many_message(search_params=None, **kwargs):
    #if search_params not in query search_params is empty dict
    if not search_params:
        raise ProcessingException(message='Forbidden',
                                  status_code=403)
    if 'filters' not in search_params:
        raise ProcessingException(message='Forbidden',
                                  status_code=403)
    for field in search_params['filters']:
        if field['name'] == 'inbox_id' and field['op'] == 'eq':
            break
    else:
        raise ProcessingException(message='Forbidden',
                                  status_code=403)


def post_get_many_message(result=None, **kwargs):
    if result['objects']:
        _check_single_inbox(result['objects'][0]['inbox_id'])
