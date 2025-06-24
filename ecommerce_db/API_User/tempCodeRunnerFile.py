
configs = get_dataset_config_names("McAuley-Lab/Amazon-Reviews-2023")

category_names = sorted(set(
    name.replace("raw_meta_", "").replace("raw_review_", "")
    for name in configs
    if name.startswith("raw_meta_")
))

existing = set(Category.objects.values_list('name', flat=True))
to_create = [Category(name=n) for n in category_names if n not in existing]

if to_create:
    Category.objects.bulk_create(to_create)