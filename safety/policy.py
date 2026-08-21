def authorize(action,human_approved=False):
 c={"release_schedule","override_constraint","commit_inventory"}
 return human_approved if action in c else True