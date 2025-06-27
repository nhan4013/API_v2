# import pickle
# import os
# from django.conf import settings
# from API_User.models import User, Product

# class RecommendationService:
#     def __init__(self):
#         self.svdpp_model = self.load_model('svdpp_user_item_model.pkl')  # Main recommendations
#         self.knn_model = self.load_model('knn_user_model.pkl')          # Similar products
    
#     def load_model(self, model_filename):
#         """Load a specific model file"""
#         pkl_file_path = os.path.join(settings.BASE_DIR, 'API_User', 'data', model_filename)
#         try:
#             with open(pkl_file_path, 'rb') as f:
#                 model = pickle.load(f)
#             print(f"{model_filename} loaded successfully")
#             return model
#         except Exception as e:
#             print(f"Error loading {model_filename}: {e}")
#             return None
    
#     def get_personalized_recommendations(self, user_id, num_recommendations=10):
#         """Use SVD++ for personalized recommendations"""
#         return self._predict_with_model(self.svdpp_model, user_id, num_recommendations)
    
#     def get_similar_products(self, product_id, num_similar=10):
#         """Use KNN for similar product suggestions"""
#         return self._get_similar_items(self.knn_model, product_id, num_similar)
    
#     def _predict_with_model(self, model, user_id, num_recommendations=10):
#         """Generate recommendations using specified model"""
#         if not model:
#             return []
        
#         try:
#             user = User.objects.get(id=user_id)
#             products = Product.objects.all()
#             recommendations = []
            
#             for product in products:
#                 try:
#                     prediction = model.predict(uid=user_id, iid=product.id)
#                     recommendations.append({
#                         'product': product,
#                         'predicted_rating': prediction.est,
#                         'product_name': product.name,
#                         'product_id': product.id,
#                         'product_price': product.price,
#                         'product_description': product.description
#                     })
#                 except Exception as e:
#                     continue
            
#             # Sort by predicted rating (highest first)
#             recommendations.sort(key=lambda x: x['predicted_rating'], reverse=True)
#             return recommendations[:num_recommendations]
            
#         except User.DoesNotExist:
#             print(f"User with id {user_id} not found")
#             return []
#         except Exception as e:
#             print(f"Error generating recommendations: {e}")
#             return []
    
#     def _get_similar_items(self, model, product_id, num_similar=10):
#         """Get similar products using KNN model"""
#         if not model:
#             return []
        
#         try:
#             target_product = Product.objects.get(id=product_id)
#             all_products = Product.objects.exclude(id=product_id)  # Exclude the target product
#             similar_products = []
            
#             # For KNN, we'll find products that similar users liked
#             # Get a sample of users who might have rated this product
#             sample_users = User.objects.all()[:50]  # Sample for performance
            
#             product_scores = {}
            
#             for user in sample_users:
#                 try:
#                     # Get rating prediction for target product
#                     target_prediction = model.predict(uid=user.id, iid=product_id)
                    
#                     # If user would rate target product highly, get their other high-rated products
#                     if target_prediction.est >= 4.0:
#                         for other_product in all_products:
#                             try:
#                                 other_prediction = model.predict(uid=user.id, iid=other_product.id)
#                                 if other_prediction.est >= 4.0:
#                                     if other_product.id not in product_scores:
#                                         product_scores[other_product.id] = {
#                                             'product': other_product,
#                                             'score': 0,
#                                             'count': 0
#                                         }
#                                     product_scores[other_product.id]['score'] += other_prediction.est
#                                     product_scores[other_product.id]['count'] += 1
#                             except:
#                                 continue
#                 except:
#                     continue
            
#             # Calculate average scores and create similar products list
#             for product_id, data in product_scores.items():
#                 if data['count'] > 0:  # At least one user rated it highly
#                     avg_score = data['score'] / data['count']
#                     similar_products.append({
#                         'product': data['product'],
#                         'similarity_score': avg_score,
#                         'product_name': data['product'].name,
#                         'product_id': data['product'].id,
#                         'product_price': data['product'].price,
#                         'based_on_users': data['count']
#                     })
            
#             # Sort by similarity score
#             similar_products.sort(key=lambda x: x['similarity_score'], reverse=True)
#             return similar_products[:num_similar]
            
#         except Product.DoesNotExist:
#             print(f"Product with id {product_id} not found")
#             return []
#         except Exception as e:
#             print(f"Error finding similar products: {e}")
#             return []
    
#     def predict_user_product_rating(self, user_id, product_id, use_svdpp=True):
#         """Predict rating for specific user-product pair"""
#         model = self.svdpp_model if use_svdpp else self.knn_model
#         model_name = "SVD++" if use_svdpp else "KNN"
        
#         if not model:
#             return None
        
#         try:
#             prediction = model.predict(uid=user_id, iid=product_id)
#             user = User.objects.get(id=user_id)
#             product = Product.objects.get(id=product_id)
            
#             return {
#                 'user_id': user_id,
#                 'user_name': user.username,
#                 'product_id': product_id,
#                 'product_name': product.name,
#                 'predicted_rating': round(prediction.est, 2),
#                 'model_used': model_name,
#                 'prediction_details': prediction.details if hasattr(prediction, 'details') else None
#             }
#         except Exception as e:
#             print(f"Prediction error: {e}")
#             return None
    
#     def get_hybrid_recommendations(self, user_id, num_recommendations=10):
#         """Combine both models for hybrid recommendations"""
#         svdpp_recs = self.get_personalized_recommendations(user_id, num_recommendations * 2)
        
#         # Weight SVD++ recommendations higher (70%) and add variety from KNN (30%)
#         hybrid_recs = []
        
#         # Add top SVD++ recommendations
#         for i, rec in enumerate(svdpp_recs[:int(num_recommendations * 0.7)]):
#             rec['recommendation_type'] = 'personalized'
#             rec['rank'] = i + 1
#             hybrid_recs.append(rec)
        
#         return hybrid_recs[:num_recommendations]

# # Global service instance
# recommendation_service = RecommendationService()


import pickle
import os
import zipfile
from django.conf import settings
from huggingface_hub import hf_hub_download
import requests
from API_User.models import User, Product

class RecommendationService:
    def __init__(self):
        self.download_models_if_needed()
        self.svdpp_model = self.load_model('svdpp_user_item_model.pkl')
        self.knn_model = self.load_model('knn_user_model.pkl')
    
    def download_models_if_needed(self):
        """Download models from Hugging Face Hub"""
        data_dir = os.path.join(settings.BASE_DIR, 'API_User', 'data')
        os.makedirs(data_dir, exist_ok=True)
        
        repo_id = "meownamsero/product_recommend"
        models = ['knn_user_model.pkl', 'svdpp_user_item_model.pkl']
        
        for model_name in models:
            local_path = os.path.join(data_dir, model_name)
            
            if not os.path.exists(local_path):
                print(f"Downloading {model_name} from Hugging Face Hub...")
                try:
                    downloaded_path = hf_hub_download(
                        repo_id=repo_id, 
                        filename=model_name,
                        cache_dir=data_dir
                    )
                    
                    # Move to expected location if needed
                    import shutil
                    shutil.copy2(downloaded_path, local_path)
                    print(f"✅ Downloaded {model_name}")
                    
                except Exception as e:
                    print(f"❌ Error downloading {model_name}: {e}")
            else:
                print(f"{model_name} already exists")
    
    def load_model(self, model_filename):
        """Load model from local data directory"""
        data_dir = os.path.join(settings.BASE_DIR, 'API_User', 'data')
        pkl_file_path = os.path.join(data_dir, model_filename)
        
        # Check if file exists
        if not os.path.exists(pkl_file_path):
            print(f"Model file not found: {pkl_file_path}")
            
            # Try to find the file with different names in the data directory
            possible_files = []
            if os.path.exists(data_dir):
                for file in os.listdir(data_dir):
                    if file.endswith('.pkl'):
                        possible_files.append(file)
                
                if possible_files:
                    print(f"Available pickle files: {possible_files}")
                    
                    # Try to match by keywords
                    if 'svdpp' in model_filename.lower():
                        for file in possible_files:
                            if 'svd' in file.lower():
                                pkl_file_path = os.path.join(data_dir, file)
                                print(f"Using {file} for SVD++ model")
                                break
                    elif 'knn' in model_filename.lower():
                        for file in possible_files:
                            if 'knn' in file.lower():
                                pkl_file_path = os.path.join(data_dir, file)
                                print(f"Using {file} for KNN model")
                                break
            
            if not os.path.exists(pkl_file_path):
                print(f"Could not find suitable model file for {model_filename}")
                return None
        
        try:
            file_size = os.path.getsize(pkl_file_path)
            print(f"Loading {model_filename} (size: {file_size} bytes)")
            
            # Validate file before loading
            with open(pkl_file_path, 'rb') as f:
                first_bytes = f.read(20)
                f.seek(0)  # Reset file pointer
                
                # Check if it's a valid pickle file
                if first_bytes.startswith(b'<') or b'<html' in first_bytes.lower():
                    print(f"Error: {model_filename} appears to be HTML, not a pickle file")
                    return None
                
                # Load the model
                model = pickle.load(f)
            
            print(f"{model_filename} loaded successfully")
            print(f"Model type: {type(model)}")
            return model
            
        except Exception as e:
            print(f"Error loading {model_filename}: {e}")
            return None
    def get_personalized_recommendations(self, user_id, num_recommendations=10):
        """Use SVD++ for personalized recommendations"""
        return self._predict_with_model(self.svdpp_model, user_id, num_recommendations)
    
    def get_similar_products(self, product_id, num_similar=10):
        """Use KNN for similar product suggestions"""
        return self._get_similar_items(self.knn_model, product_id, num_similar)
    
    def _predict_with_model(self, model, user_id, num_recommendations=10):
        """Generate recommendations using specified model"""
        if not model:
            return []
        
        try:
            user = User.objects.get(id=user_id)
            products = Product.objects.all()
            recommendations = []
            
            for product in products:
                try:
                    prediction = model.predict(uid=user_id, iid=product.id)
                    recommendations.append({
                        'product': product,
                        'predicted_rating': prediction.est,
                        'product_name': product.name,
                        'product_id': product.id,
                        'product_price': product.price,
                        'product_description': product.description
                    })
                except Exception as e:
                    continue
            
            # Sort by predicted rating (highest first)
            recommendations.sort(key=lambda x: x['predicted_rating'], reverse=True)
            return recommendations[:num_recommendations]
            
        except User.DoesNotExist:
            print(f"User with id {user_id} not found")
            return []
        except Exception as e:
            print(f"Error generating recommendations: {e}")
            return []
    
    def _get_similar_items(self, model, product_id, num_similar=10):
        """Get similar products using KNN model"""
        if not model:
            return []
        
        try:
            target_product = Product.objects.get(id=product_id)
            all_products = Product.objects.exclude(id=product_id)  # Exclude the target product
            similar_products = []
            
            # For KNN, we'll find products that similar users liked
            # Get a sample of users who might have rated this product
            sample_users = User.objects.all()[:50]  # Sample for performance
            
            product_scores = {}
            
            for user in sample_users:
                try:
                    # Get rating prediction for target product
                    target_prediction = model.predict(uid=user.id, iid=product_id)
                    
                    # If user would rate target product highly, get their other high-rated products
                    if target_prediction.est >= 4.0:
                        for other_product in all_products:
                            try:
                                other_prediction = model.predict(uid=user.id, iid=other_product.id)
                                if other_prediction.est >= 4.0:
                                    if other_product.id not in product_scores:
                                        product_scores[other_product.id] = {
                                            'product': other_product,
                                            'score': 0,
                                            'count': 0
                                        }
                                    product_scores[other_product.id]['score'] += other_prediction.est
                                    product_scores[other_product.id]['count'] += 1
                            except:
                                continue
                except:
                    continue
            
            # Calculate average scores and create similar products list
            for product_id, data in product_scores.items():
                if data['count'] > 0:  # At least one user rated it highly
                    avg_score = data['score'] / data['count']
                    similar_products.append({
                        'product': data['product'],
                        'similarity_score': avg_score,
                        'product_name': data['product'].name,
                        'product_id': data['product'].id,
                        'product_price': data['product'].price,
                        'based_on_users': data['count']
                    })
            
            # Sort by similarity score
            similar_products.sort(key=lambda x: x['similarity_score'], reverse=True)
            return similar_products[:num_similar]
            
        except Product.DoesNotExist:
            print(f"Product with id {product_id} not found")
            return []
        except Exception as e:
            print(f"Error finding similar products: {e}")
            return []
    
    def predict_user_product_rating(self, user_id, product_id, use_svdpp=True):
        """Predict rating for specific user-product pair"""
        model = self.svdpp_model if use_svdpp else self.knn_model
        model_name = "SVD++" if use_svdpp else "KNN"
        
        if not model:
            return None
        
        try:
            prediction = model.predict(uid=user_id, iid=product_id)
            user = User.objects.get(id=user_id)
            product = Product.objects.get(id=product_id)
            
            return {
                'user_id': user_id,
                'user_name': user.username,
                'product_id': product_id,
                'product_name': product.name,
                'predicted_rating': round(prediction.est, 2),
                'model_used': model_name,
                'prediction_details': prediction.details if hasattr(prediction, 'details') else None
            }
        except Exception as e:
            print(f"Prediction error: {e}")
            return None
    
    def get_hybrid_recommendations(self, user_id, num_recommendations=10):
        """Combine both models for hybrid recommendations"""
        svdpp_recs = self.get_personalized_recommendations(user_id, num_recommendations * 2)
        
        # Weight SVD++ recommendations higher (70%) and add variety from KNN (30%)
        hybrid_recs = []
        
        # Add top SVD++ recommendations
        for i, rec in enumerate(svdpp_recs[:int(num_recommendations * 0.7)]):
            rec['recommendation_type'] = 'personalized'
            rec['rank'] = i + 1
            hybrid_recs.append(rec)
        
        return hybrid_recs[:num_recommendations]

# Global service instance
recommendation_service = RecommendationService()