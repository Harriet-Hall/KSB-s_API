def check_for_duplicates(ksbs, post_payload):

    type = post_payload["ksb_type"].capitalize()
    code = post_payload["ksb_code"]
    description = post_payload["description"]

    for ksb in ksbs:
        if ksb.ksb_type == type and ksb.ksb_code == code or ksb.description == description:
            return True
            
