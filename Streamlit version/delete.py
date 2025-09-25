# cleanup.py
import os
import shutil

def cleanup_streamlit_app():
    # Files and folders to delete
    to_delete = [
        # Cache and logs
        'cache/',
        'analysis.log',
        'app.log', 
        'processing.log',
        
        # Raw data folders
        'data/data/resumes/',
        'data/resumes/raw/',
        'data/resumes/annotations/',
        'data/jobs/raw/',
        'data/courses/raw/',
        'data/skills/raw/',
        
        # Development files
        'feedback/',
        'tests/',
        'setup.py',
        'setup_dirs.py',
        'run_conversion.py',
    ]
    
    for item in to_delete:
        if os.path.exists(item):
            if os.path.isdir(item):
                shutil.rmtree(item)
                print(f"Deleted folder: {item}")
            else:
                os.remove(item)
                print(f"Deleted file: {item}")
        else:
            print(f"Not found: {item}")
    
    print("Cleanup completed!")

if __name__ == "__main__":
    cleanup_streamlit_app()