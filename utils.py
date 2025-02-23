def check_for_duplicates(ksbs, post_payload):
            for ksb in ksbs:
                if ksb.ksb_type == post_payload.json["ksb_type"] and ksb.ksb_code == post_payload.json["ksb_code"]:
                    return True