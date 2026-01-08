import sys
import os

def test_pypi_package():
    print("🧪 Testing TheUltimateRAG PyPI Package...")
    
    # 1. Check Import
    try:
        import theultimaterag
        print(f"✅ Successfully imported 'theultimaterag'")
        print(f"   Location: {os.path.dirname(theultimaterag.__file__)}")
    except ImportError:
        print("❌ Failed to import 'theultimaterag'. Did you run 'pip install theultimaterag'?")
        return

    # 2. Check Core Modules
    try:
        from theultimaterag.core.container import rag_engine
        print("✅ Successfully imported 'rag_engine'")
    except ImportError as e:
        print(f"❌ Failed to import core modules: {e}")
        return

    # 3. Check CLI Entry Point (Simulated)
    try:
        from theultimaterag.server import start
        print("✅ Entry point 'server.start' is available")
    except ImportError as e:
        print(f"❌ Failed to find entry point: {e}")
        return
        
    print("\n🎉 The package is installed and functional!")
    print("Run 'theultimaterag start' to launch the server.")

if __name__ == "__main__":
    test_pypi_package()
