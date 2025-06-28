import requests
import os
import pickle

def download_file(url, output_path):
    """Download a single file with progress tracking and integrity check"""
    try:
        print(f"Starting download to: {output_path}")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Download to temporary file first
        temp_path = output_path + '.tmp'
        
        with open(temp_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024*1024):  # 1MB chunks
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        progress = (downloaded / total_size) * 100
                        print(f"Progress: {progress:.1f}%")
        
        # Verify file integrity
        try:
            with open(temp_path, 'rb') as f:
                pickle.load(f)
            print("✅ File integrity verified")
        except Exception as e:
            print(f"❌ Downloaded file is corrupted: {e}")
            os.remove(temp_path)
            return False
        
        # Move to final location
        os.rename(temp_path, output_path)
        
        file_size = os.path.getsize(output_path) / (1024*1024)
        print(f"✅ Downloaded {os.path.basename(output_path)} ({file_size:.1f} MB)")
        return True
        
    except Exception as e:
        print(f"❌ Error downloading {os.path.basename(output_path)}: {e}")
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return False

def setup_models():
    """Download both models to Railway volume"""
    # Check if we're on Railway with volume mount
    if os.path.exists('/data') and os.access('/data', os.W_OK):
        base_path = '/data'
        print("Using Railway volume: /data")
    else:
        # Fallback for local testing
        base_path = os.path.join(os.path.dirname(__file__), 'data')
        print(f"Using local directory: {base_path}")
    
    models = {
        'knn_user_model.pkl': 'https://huggingface.co/meownamsero/product_recommend/resolve/main/knn_user_model.pkl',
        'svdpp_user_item_model.pkl': 'https://huggingface.co/meownamsero/product_recommend/resolve/main/svdpp_user_item_model.pkl'
    }
    
    for model_name, url in models.items():
        output_path = os.path.join(base_path, model_name)
        
        if os.path.exists(output_path):
            # Check if existing file is valid
            try:
                with open(output_path, 'rb') as f:
                    pickle.load(f)
                print(f"✅ {model_name} already exists and is valid")
                continue
            except Exception:
                print(f"⚠️ Existing {model_name} is corrupted, re-downloading...")
                os.remove(output_path)
        
        print(f"\nDownloading {model_name}...")
        success = False
        
        # Retry up to 3 times
        for attempt in range(3):
            print(f"Attempt {attempt + 1}/3")
            if download_file(url, output_path):
                success = True
                break
            else:
                print(f"Attempt {attempt + 1} failed")
                if os.path.exists(output_path):
                    os.remove(output_path)
        
        if not success:
            print(f"❌ Failed to download {model_name} after 3 attempts")
        else:
            print(f"✅ {model_name} setup complete")
    
    print("\n🎉 Model setup completed!")

if __name__ == "__main__":
    setup_models()