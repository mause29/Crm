#!/usr/bin/env python3
"""
Script to generate and save the OpenAPI specification
"""
import json
import requests
from pathlib import Path

def generate_openapi_spec():
    """Generate OpenAPI specification from running server"""
    try:
        # Make request to OpenAPI endpoint
        response = requests.get("http://localhost:8000/openapi.json", timeout=10)

        if response.status_code == 200:
            spec = response.json()

            # Save to file
            docs_dir = Path("docs")
            docs_dir.mkdir(exist_ok=True)

            with open(docs_dir / "openapi_spec.json", "w", encoding="utf-8") as f:
                json.dump(spec, f, indent=2, ensure_ascii=False)

            print("✅ OpenAPI specification generated successfully!")
            print(f"📄 Saved to: {docs_dir / 'openapi_spec.json'}")

            # Also save as YAML
            try:
                import yaml
                with open(docs_dir / "openapi_spec.yaml", "w", encoding="utf-8") as f:
                    yaml.dump(spec, f, default_flow_style=False, allow_unicode=True)
                print(f"📄 Also saved as YAML: {docs_dir / 'openapi_spec.yaml'}")
            except ImportError:
                print("⚠️  PyYAML not installed, skipping YAML export")

            return spec
        else:
            print(f"❌ Failed to fetch OpenAPI spec: HTTP {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to server: {e}")
        print("💡 Make sure the FastAPI server is running on http://localhost:8000")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None

if __name__ == "__main__":
    generate_openapi_spec()
