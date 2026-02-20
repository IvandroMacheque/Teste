import os

def get_exports_dir():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    export_dir = os.path.join(base_dir, "assets", "exports")
    
    if not os.path.exists(export_dir):
        os.makedirs(export_dir, exist_ok=True)
        
    return export_dir

def get_download_url(filename):
    return f"/exports/{filename}"