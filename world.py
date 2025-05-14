from perception import detect_object

def get_current_scene(objects_of_interest: list[str]):
    visible = []
    for name in objects_of_interest:
        result = detect_object(name)
        if result:
            visible.append({
                "name": name,
                "location": result["position"]
            })
    return visible
