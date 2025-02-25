def check_for_valid_updates(ksbs, ksb_to_update):
    type = ksb_to_update.ksb_type
    code = ksb_to_update.ksb_code
    description = ksb_to_update.description

    for ksb in ksbs:
        if ksb.id == ksb_to_update.id:
            continue  

        if (
            (description == ksb.description and type == ksb.ksb_type and code == ksb.ksb_code) 
            or (type == ksb.ksb_type and code == ksb.ksb_code)
            or (type == ksb.ksb_type and description == ksb.description) 
        ):
            return True

    return False
