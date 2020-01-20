from django.contrib.auth.models import Group, Permission


def CuratorGroup(u):
    group, created = Group.objects.get_or_create(name="Curators")
    prem = [
        # "Can view course",
        "add_opencourse",
        "add_opencontent",
        "change_opencontent",
        "delete_opencontent",
        "view_opencontent",
        "add_opencourse",
        "change_opencourse",
        "delete_opencourse",
        "view_opencourse",
        "add_openmodule",
        "change_openmodule",
        "delete_openmodule",
        "view_openmodule",
        "add_text",
        "change_text",
        "delete_text",
        "view_text",
        "add_video",
        "change_video",
        "delete_video",
        "view_video",
        "add_answer",
        "change_answer",
        "delete_answer",
        "view_answer",
    ]
    print("asdas")
    for p in prem:
        add_prem = Permission.objects.get(codename=p)
        group.permissions.add(add_prem)
    u.groups.add(group)
    return u
