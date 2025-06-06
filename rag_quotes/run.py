import os
import subprocess
import argparse
import sys

def setup_environment():
    """Setup the environment and install dependencies"""
    print("Setting up environment...")
    # Install dependencies
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Dependencies installed")
    except Exception as e:
        print(f"Error installing dependencies: {e}")

def create_embeddings():
    """Create embeddings for the quotes"""
    print("Creating embeddings...")
    # Import the embeddings module
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from models.embeddings import main as embeddings_main
    
    # Run the embeddings creation
    embeddings_main()
    print("Embeddings created")

def run_app():
    """Run the Streamlit app"""
    print("Running the Streamlit app...")
    app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app", "app.py")
    subprocess.run(["streamlit", "run", app_path])

def main():
    """Main function to run the application"""
    parser = argparse.ArgumentParser(description="Shailosophy Quotes RAG Application")
    parser.add_argument("--setup", action="store_true", help="Setup environment and install dependencies")
    parser.add_argument("--embeddings", action="store_true", help="Create embeddings for quotes")
    parser.add_argument("--run", action="store_true", help="Run the Streamlit app")
    
    args = parser.parse_args()
    
    # If no arguments provided, run all steps
    if not (args.setup or args.embeddings or args.run):
        args.setup = True
        args.embeddings = True
        args.run = True
    
    if args.setup:
        setup_environment()
    
    if args.embeddings:
        create_embeddings()
    
    if args.run:
        run_app()

if __name__ == "__main__":
    main() 