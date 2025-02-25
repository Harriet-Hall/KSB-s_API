from database import Ksb

def check_for_duplicates(ksbs, post_payload):
    if isinstance(post_payload, dict):
        type = post_payload["ksb_type"].capitalize()
        code = post_payload["ksb_code"]
        description = post_payload["description"]
    elif isinstance(post_payload, Ksb):
        type = post_payload.ksb_type
        code = post_payload.ksb_code
        description = post_payload.description
    else:
        raise ValueError("Invalid post_payload type")

    for ksb in ksbs:
        if (
            ksb.ksb_type == type and
            ksb.ksb_code == code and
            ksb.description == description
        ):
            return True 
    return False  