from app import app
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print("\n=================================================")
    print("🚀 Application is running!")
    print("📱 Visit: https://admin-panel-site-axil.onrender.com")
    print("=================================================\n")
    app.run(host='0.0.0.0', port=port)