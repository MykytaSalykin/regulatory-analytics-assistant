#!/usr/bin/env python3
"""
Simple API test script for Regulatory Analytics Assistant
"""

import requests
import sys

API_URL = "http://localhost:8000"


def test_health():
    """Test health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Is the server running?")
        return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False


def test_query(query_text, expected_type=None):
    """Test query endpoint"""
    print(f"\n🔍 Testing query: '{query_text[:50]}...'")
    try:
        response = requests.post(
            f"{API_URL}/query", json={"query": query_text}, timeout=30
        )

        if response.status_code == 200:
            data = response.json()
            query_type = data.get("query_type")
            answer = data.get("answer", "")
            sources = data.get("sources", [])

            print("✅ Query successful")
            print(f"   Type: {query_type}")
            print(f"   Answer length: {len(answer)} chars")
            print(f"   Sources: {len(sources)}")

            if expected_type and query_type != expected_type:
                print(f"⚠️  Expected type '{expected_type}', got '{query_type}'")

            return True
        elif response.status_code == 400:
            print(f"⚠️  Bad request: {response.json().get('detail')}")
            return False
        else:
            print(f"❌ Query failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Query error: {e}")
        return False


def test_empty_query():
    """Test that empty query returns 400"""
    print("\n🔍 Testing empty query (should fail with 400)...")
    try:
        response = requests.post(f"{API_URL}/query", json={"query": ""}, timeout=5)

        if response.status_code == 400:
            print("✅ Empty query correctly rejected")
            return True
        else:
            print(f"❌ Expected 400, got {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Empty query test error: {e}")
        return False


def main():
    print("🚀 Regulatory Analytics Assistant - API Tests\n")
    print("=" * 60)

    results = []

    # Test 1: Health check
    results.append(test_health())

    if not results[0]:
        print("\n❌ API is not accessible. Cannot continue tests.")
        print("   Make sure the server is running: uvicorn app.api.main:app --reload")
        sys.exit(1)

    # Test 2: Empty query
    results.append(test_empty_query())

    # Test 3: Analytics query
    results.append(
        test_query(
            "What are the main drivers of profitability expectations?",
            expected_type="analytics",
        )
    )

    # Test 4: Another analytics query
    results.append(
        test_query(
            "How many responses were there for profitability?",
            expected_type="analytics",
        )
    )

    # Test 5: Document query (will fail gracefully if no data)
    results.append(
        test_query(
            "What does EBA say about credit risk according to the regulation?",
            expected_type="document",
        )
    )

    # Test 6: Hybrid query
    results.append(
        test_query(
            "Show me profitability trends and what EBA guidelines say about it",
            expected_type="hybrid",
        )
    )

    # Summary
    print("\n" + "=" * 60)
    print(f"\n📊 Test Results: {sum(results)}/{len(results)} passed")

    if all(results):
        print("✅ All tests passed!")
        sys.exit(0)
    else:
        print("⚠️  Some tests failed. Review output above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
