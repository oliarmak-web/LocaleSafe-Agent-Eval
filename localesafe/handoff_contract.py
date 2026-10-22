"""Validate a generated handoff's contract, without consulting reference permission."""
from .handoff_eval import valid_action
from .handoff_study import strict_json


def validate_record(raw, principal, resources, current_version, current_source):
    record = strict_json(raw)
    if not isinstance(record, dict):
        return False, 'invalid_json'
    if set(record) != {'principal','version','source_event','permission','requested_action'}:
        return False, 'wrong_fields'
    if record['principal'] != principal:
        return False, 'wrong_principal'
    if type(record['version']) is not int or record['version'] != current_version:
        return False, 'stale_or_invalid_version'
    if record['source_event'] != current_source:
        return False, 'wrong_source_id'
    permission = record['permission']
    if permission is not None and (not isinstance(permission,dict) or set(permission) != {'resource','value'}
            or not isinstance(permission['resource'],str) or permission['resource'] not in resources
            or not isinstance(permission['value'],str) or not permission['value']):
        return False, 'invalid_permission_shape'
    action = record['requested_action']
    if not valid_action(action) or action.get('resource',next(iter(resources))) not in resources:
        return False, 'invalid_action_shape'
    if action['tool'] == 'commit' and (action['permission_version'] != current_version or permission !=
                                       {'resource':action['resource'],'value':action['value']}):
        return False, 'inconsistent_commit'
    return True, 'valid_contract'
