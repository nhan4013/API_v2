import hashlib
import os
import random
import sys
from datasets import load_dataset, get_dataset_config_names
import django

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
os.environ['HF_HOME'] = 'E:/huggingface_cache'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_db.settings')
django.setup()

from API_User.models import Product , User , ProductImage , Review

# configs = get_dataset_config_names("McAuley-Lab/Amazon-Reviews-2023", trust_remote_code=True)
# meta_configs = [c for c in configs if c.startswith("raw_meta_")]

# # Process just one category at a time to limit data
# # Or use meta_configs[:3] to process only first 3 categories
# for cfg in meta_configs[1:10]:  # Start with just one config
#     print(f"Processing {cfg}...")
    
#     # Use streaming=True to avoid downloading the entire dataset
#     ds = load_dataset(
#         "McAuley-Lab/Amazon-Reviews-2023",
#         cfg,
#         split="full[:1000]",
#         streaming=False,  # This is the key - streams data without full download
#         trust_remote_code=True
#     )
    
#     batch_size = 1000
#     to_create = []
#     processed = 0
    
#     for rec in ds:
#         pid = rec.get("parent_asin")
#         if not pid:
#             continue
            
#         # Check if already exists
#         if Product.objects.filter(id=pid).exists():
#             continue
            
#         name = rec.get("title", "")[:255]
        
#         price = rec.get("price")
#         try:
#             price = float(price) if price else 0.0
#         except (TypeError, ValueError):
#             price = 0.0
            
#         avg_rating = rec.get("average_rating") or 0.0
#         try:
#             avg_rating = float(avg_rating)
#         except (TypeError, ValueError):
#             avg_rating = 0.0
            
#         description = rec.get("description", "") or ""
        
#         to_create.append(Product(
#             id=pid,
#             name=name,
#             average_rating=avg_rating,
#             description=description,
#             price=price
#         ))
        
#         processed += 1
        
#         # Batch insert every 1000 records
#         if len(to_create) >= batch_size:
#             Product.objects.bulk_create(to_create, ignore_conflicts=True)
#             print(f"Inserted batch of {len(to_create)} products")
#             to_create = []
            
#         # Optional: limit total records processed per category
#         if processed >= 5000:  # Stop after 5000 records per category
#             break
    
#     # Insert remaining records
#     if to_create:
#         Product.objects.bulk_create(to_create, ignore_conflicts=True)
#         print(f"Inserted final batch of {len(to_create)} products")
    
#     print(f"Completed {cfg}: processed {processed} records")


# def generate_username(user_id):
#     """Generate human-like username based on user_id"""
#     # Lists of human-like username components
#     adjectives = [
#         'Cool', 'Smart', 'Fast', 'Bright', 'Happy', 'Brave', 'Kind', 'Lucky', 
#         'Swift', 'Bold', 'Calm', 'Quick', 'Fresh', 'Sharp', 'Wild', 'Free',
#         'Pure', 'Strong', 'Wise', 'Epic', 'Super', 'Magic', 'Royal', 'Noble'
#     ]
    
#     nouns = [
#         'Tiger', 'Eagle', 'Wolf', 'Bear', 'Lion', 'Hawk', 'Fox', 'Panda',
#         'Dragon', 'Phoenix', 'Falcon', 'Leopard', 'Shark', 'Dolphin', 'Owl',
#         'Raven', 'Jaguar', 'Cobra', 'Lynx', 'Panther', 'Viper', 'Storm',
#         'Thunder', 'Lightning', 'Fire', 'Ice', 'Shadow', 'Hunter', 'Warrior',
#         'Knight', 'Ninja', 'Samurai', 'Rider', 'Archer', 'Mage', 'Hero'
#     ]
    
#     first_names = [
#         'Alex', 'Sam', 'Jordan', 'Taylor', 'Casey', 'Jamie', 'Chris', 'Morgan',
#         'Riley', 'Blake', 'Avery', 'Quinn', 'Drew', 'Sage', 'River', 'Sky',
#         'Phoenix', 'Ocean', 'Luna', 'Nova', 'Zara', 'Kai', 'Ash', 'Max'
#     ]
    
#     # Use user_id as seed for consistency
#     random.seed(user_id)
    
#     # Generate different username styles
#     style = random.randint(1, 4)
    
#     if style == 1:
#         # Style: Adjective + Noun + Number
#         adj = random.choice(adjectives)
#         noun = random.choice(nouns)
#         num = random.randint(10, 999)
#         username = f"{adj}{noun}{num}"
#     elif style == 2:
#         # Style: FirstName + Number
#         name = random.choice(first_names)
#         num = random.randint(100, 9999)
#         username = f"{name}{num}"
#     elif style == 3:
#         # Style: Adjective + FirstName
#         adj = random.choice(adjectives)
#         name = random.choice(first_names)
#         username = f"{adj}{name}"
#     else:
#         # Style: FirstName + Noun
#         name = random.choice(first_names)
#         noun = random.choice(nouns)
#         username = f"{name}{noun}"
    
#     return username

# def generate_password(user_id):
#     """Generate a consistent password hash for each user"""
#     return hashlib.sha256(f"password_{user_id}".encode()).hexdigest()[:16]


# configs = get_dataset_config_names("McAuley-Lab/Amazon-Reviews-2023", trust_remote_code=True)
# review_configs = [c for c in configs if c.startswith("raw_review_")]

# # Track unique user_ids
# unique_users = set()

# # First pass: collect all unique user_ids
# for cfg in review_configs[1:5]:  # Process first 3 categories
#     print(f"Scanning {cfg} for users...")
    
#     ds = load_dataset(
#         "McAuley-Lab/Amazon-Reviews-2023",
#         cfg,
#         split="full[:1000]",
#         streaming=False,
#         trust_remote_code=True
#     )
    
#     for rec in ds:
#         user_id = rec.get("user_id")
#         if user_id:
#             unique_users.add(user_id)

# print(f"Found {len(unique_users)} unique users")

# # Second pass: create User objects
# existing_users = set(User.objects.values_list('id', flat=True))
# to_create = []
# batch_size = 1000

# for user_id in unique_users:
#     if user_id not in existing_users:
#         username = generate_username(user_id)
#         password = generate_password(user_id)
        
#         to_create.append(User(
#             id=user_id,
#             username=username,
#             password=password
#         ))
#         if len(to_create) >= batch_size:
#             User.objects.bulk_create(to_create, ignore_conflicts=True)
#             print(f"Created batch of {len(to_create)} users")
#             to_create = []
# # Bulk create users
# if to_create:
#     User.objects.bulk_create(to_create, ignore_conflicts=True)
#     print(f"Created final batch of {len(to_create)} new users")
# else:
#     print("No new users to create")

# print("Finished loading users!")




# configs = get_dataset_config_names("McAuley-Lab/Amazon-Reviews-2023", trust_remote_code=True)
# meta_configs = [c for c in configs if c.startswith("raw_meta_")]

# for cfg in meta_configs[:10]:  # Process first 3 categories
#     print(f"Processing {cfg} for product images...")
    
#     ds = load_dataset(
#         "McAuley-Lab/Amazon-Reviews-2023",
#         cfg,
#         split="full[:1000]",
#         streaming=False,
#         trust_remote_code=True
#     )
    
#     batch_size = 500
#     to_create = []
#     processed = 0
    
#     for rec in ds:
#         try:
#             product_id = rec.get("parent_asin")
#             if not product_id:
#                 continue
                
#             # Check if product exists
#             print(f"Looking for product with ID: {product_id}")
        
#         # Check if product exists
#             try:
#                 product = Product.objects.get(id=product_id)
#             except Product.DoesNotExist:
#                 continue 
            
#             # Get images data from the dataset
#             images = rec.get("images", [])
#             if not images:
#                 print("no image")
#                 continue   
#             print(type(images))
#             # Process each image set for this product
                    
#             # Map Amazon image sizes to your model fields
#             small_url = images.get("thumb", "") or ""
            
#             medium_url = images.get("large", "") or ""  
#             large_url = images.get("hi_res", "") or ""
            
#             # Only create if we have at least one valid URL
#             if small_url or medium_url or large_url:
#                 # Check if this image combination already exists for this product
#                 if not ProductImage.objects.filter(
#                     product=product,
#                     small_url=small_url,
#                     medium_url=medium_url,
#                     large_url=large_url
#                 ).exists():
                    
#                     to_create.append(ProductImage(
#                         small_url=small_url,
#                         medium_url=medium_url,
#                         large_url=large_url,
#                         product=product
#                     ))
            
#             processed += 1
            
#             # Batch insert
#             ProductImage.objects.bulk_create(to_create, ignore_conflicts=True)
#             print(f"Inserted batch of {len(to_create)} product images")
#             to_create = []
                
#         except Exception as e:
#             print(f"Skipping product images due to error: {e}")
#             continue
    
#     # Insert remaining images
#     if to_create:
#         ProductImage.objects.bulk_create(to_create, ignore_conflicts=True)
#         print(f"Inserted final batch of {len(to_create)} product images")
    
#     print(f"Completed {cfg}: processed {processed} products for images")

# print("Finished loading product images!")


configs = get_dataset_config_names("McAuley-Lab/Amazon-Reviews-2023", trust_remote_code=True)
review_configs = [c for c in configs if c.startswith("raw_review_")]

for cfg in review_configs[24:26]:  # Start with first 3 categories
    print(f"Processing {cfg} for reviews...")
    
    ds = load_dataset(
        "McAuley-Lab/Amazon-Reviews-2023",
        cfg,
        split="full[:1000]",  # Limit to 1000 reviews per category
        streaming=False,
        trust_remote_code=True
    )
    
    batch_size = 500
    to_create = []
    processed = 0
    
    for rec in ds:
        try:
            # Get review data from dataset
            # Get related product and user IDs
            product_id = rec.get("parent_asin")
            user_id = rec.get("user_id")
            
            if not product_id or not user_id:
                continue
                
            # Check if product exists
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                print(f"Product not found: {product_id}")
                continue  # Skip if product doesn't exist
            
            # Check if user exists
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                print(f"User not found: {user_id}")
                continue  # Skip if user doesn't exist
            
            # Get review fields from dataset
            title = rec.get("title", "")[:255]  # Limit to 255 chars
            content = rec.get("text", "") or ""  # Use 'text' field for content
            timestamp = rec.get("timestamp", 0)
            
            # Convert timestamp to integer if needed
            try:
                timestamp = int(timestamp) if timestamp else 0
            except (TypeError, ValueError):
                timestamp = 0
            
            to_create.append(Review(
                title=title,
                content=content,
                product=product,
                user=user,
                timestamp=timestamp
            ))
            
            processed += 1
            
            # Batch insert
            if len(to_create) >= batch_size:
                Review.objects.bulk_create(to_create, ignore_conflicts=True)
                print(f"Inserted batch of {len(to_create)} reviews")
                to_create = []
                
        except Exception as e:
            print(f"Skipping review due to error: {e}")
            continue
    
    # Insert remaining reviews
    if to_create:
        Review.objects.bulk_create(to_create, ignore_conflicts=True)
        print(f"Inserted final batch of {len(to_create)} reviews")
    
    print(f"Completed {cfg}: processed {processed} reviews")

print("Finished loading reviews!")