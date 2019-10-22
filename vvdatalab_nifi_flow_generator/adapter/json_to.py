from nipyapi import canvas

def to_process_group(json_process_group):
    try:
        process_group = canvas.get_process_group(
            json_process_group["parent_group_id"],'id')
        process_group.revision.version = 0

        return process_group

    except Exception as e:
        return str(e)