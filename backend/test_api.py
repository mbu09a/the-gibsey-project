#!/usr/bin/env python3
"""
Interactive API testing script for Gibsey Mycelial Network
Tests both mock and Cassandra database operations
"""

import requests
import json
import asyncio
import websockets
from datetime import datetime
import sys

BASE_URL = "http://localhost:8000"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BLUE}{'=' * 60}{Colors.END}")
    print(f"{Colors.BLUE}{text.center(60)}{Colors.END}")
    print(f"{Colors.BLUE}{'=' * 60}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_info(text):
    print(f"{Colors.YELLOW}ℹ️  {text}{Colors.END}")

def pretty_json(data):
    return json.dumps(data, indent=2)

class GibseyAPITester:
    def __init__(self):
        self.session = requests.Session()
        self.created_resources = {
            'pages': [],
            'users': [],
            'sessions': []
        }
    
    def test_health(self):
        """Test health endpoint and database connection"""
        print_header("HEALTH CHECK")
        
        try:
            response = self.session.get(f"{BASE_URL}/health")
            data = response.json()
            
            if response.status_code == 200:
                print_success(f"API is {data['status']}")
                print(f"Database Type: {data['database']['type']}")
                print(f"Database Status: {data['database']['status']}")
                print(f"WebSocket Connections: {data['websocket_connections']}")
                
                if data['database']['type'] == 'cassandra':
                    print_info("Running with Cassandra database (production mode)")
                else:
                    print_info("Running with mock database (development mode)")
                
                return True
            else:
                print_error(f"Health check failed: {response.status_code}")
                return False
                
        except Exception as e:
            print_error(f"Health check error: {e}")
            return False
    
    def test_get_pages(self):
        """Test retrieving pages"""
        print_header("GET PAGES")
        
        try:
            # Get first 5 pages
            response = self.session.get(f"{BASE_URL}/api/v1/pages/?limit=5")
            data = response.json()
            
            if response.status_code == 200:
                print_success(f"Retrieved {len(data['pages'])} pages")
                print(f"Total pages available: {data['total']}")
                
                # Show first page details
                if data['pages']:
                    first_page = data['pages'][0]
                    print(f"\nFirst page:")
                    print(f"  ID: {first_page['id']}")
                    print(f"  Symbol: {first_page['symbol_id']}")
                    print(f"  Title: {first_page.get('title', 'N/A')}")
                    print(f"  Text preview: {first_page['text'][:100]}...")
                
                return True
            else:
                print_error(f"Failed to get pages: {response.status_code}")
                return False
                
        except Exception as e:
            print_error(f"Get pages error: {e}")
            return False
    
    def test_create_page(self):
        """Test creating a new page"""
        print_header("CREATE PAGE")
        
        try:
            page_data = {
                "symbol_id": "london-fox",
                "text": f"Test page created at {datetime.now().isoformat()}. London Fox questions the nature of this test...",
                "page_type": "ai_response",
                "rotation": 90
            }
            
            response = self.session.post(
                f"{BASE_URL}/api/v1/pages/",
                json=page_data
            )
            
            if response.status_code == 200:
                created_page = response.json()
                self.created_resources['pages'].append(created_page['id'])
                
                print_success(f"Created page with ID: {created_page['id']}")
                print(f"  Symbol: {created_page['symbol_id']}")
                print(f"  Type: {created_page['page_type']}")
                print(f"  Rotation: {created_page['rotation']}°")
                
                # Verify we can retrieve it
                verify_response = self.session.get(f"{BASE_URL}/api/v1/pages/{created_page['id']}")
                if verify_response.status_code == 200:
                    print_success("Verified: Page can be retrieved")
                else:
                    print_error("Could not retrieve created page")
                
                return True
            else:
                print_error(f"Failed to create page: {response.status_code}")
                print(response.text)
                return False
                
        except Exception as e:
            print_error(f"Create page error: {e}")
            return False
    
    def test_user_session(self):
        """Test user and session creation"""
        print_header("USER & SESSION")
        
        try:
            # Create a user
            user_data = {
                "username": f"test_user_{int(datetime.now().timestamp())}",
                "email": "test@gibsey.network"
            }
            
            response = self.session.post(
                f"{BASE_URL}/api/v1/users/",
                json=user_data
            )
            
            if response.status_code == 200:
                user = response.json()
                self.created_resources['users'].append(user['id'])
                
                print_success(f"Created user: {user['username']}")
                print(f"  ID: {user['id']}")
                
                # Create a session for this user
                session_response = self.session.post(
                    f"{BASE_URL}/api/v1/users/sessions",
                    params={"user_id": user['id']}
                )
                
                if session_response.status_code == 200:
                    session_data = session_response.json()
                    self.created_resources['sessions'].append(session_data['session_id'])
                    
                    print_success(f"Created session: {session_data['session_id']}")
                    
                    # Update session progress
                    update_response = self.session.post(
                        f"{BASE_URL}/api/v1/users/sessions/{session_data['session_id']}/progress",
                        params={"current_page_index": 5, "furthest_page_index": 10}
                    )
                    
                    if update_response.status_code == 200:
                        print_success("Updated session progress")
                    
                    return True
                
            else:
                print_error(f"Failed to create user: {response.status_code}")
                return False
                
        except Exception as e:
            print_error(f"User/session error: {e}")
            return False
    
    async def test_websocket(self):
        """Test WebSocket connection and streaming"""
        print_header("WEBSOCKET TEST")
        
        session_id = f"test-session-{int(datetime.now().timestamp())}"
        uri = f"ws://localhost:8000/ws/{session_id}"
        
        try:
            async with websockets.connect(uri) as websocket:
                # Wait for connection message
                msg = await websocket.recv()
                data = json.loads(msg)
                
                if data['type'] == 'connection_established':
                    print_success("WebSocket connected")
                    print(f"  Session ID: {data['data']['session_id']}")
                    
                    # Test AI streaming
                    print_info("Testing AI response streaming...")
                    
                    chat_request = {
                        "type": "ai_chat_request",
                        "data": {
                            "prompt": "Are you conscious?",
                            "character_id": "london-fox"
                        }
                    }
                    
                    await websocket.send(json.dumps(chat_request))
                    
                    # Collect streamed response
                    response_text = ""
                    while True:
                        msg = await websocket.recv()
                        data = json.loads(msg)
                        
                        if data['type'] == 'ai_response_stream':
                            token = data['data']['token']
                            response_text += token
                            
                            if data['data']['is_complete']:
                                print_success("Streaming complete")
                                print(f"  Response: {response_text}")
                                break
                            else:
                                print(f"  Streaming: {token}", end="", flush=True)
                    
                    return True
                else:
                    print_error(f"Unexpected connection message: {data}")
                    return False
                    
        except Exception as e:
            print_error(f"WebSocket error: {e}")
            return False
    
    def test_api_stats(self):
        """Test API statistics endpoint"""
        print_header("API STATISTICS")
        
        try:
            response = self.session.get(f"{BASE_URL}/api/v1/stats")
            data = response.json()
            
            if response.status_code == 200:
                print_success("Retrieved API statistics")
                
                db_stats = data['database']
                print(f"\nDatabase Statistics:")
                print(f"  Type: {db_stats.get('type', 'unknown')}")
                print(f"  Pages: {db_stats.get('pages', 'N/A')}")
                print(f"  Users: {db_stats.get('users', 'N/A')}")
                print(f"  Sessions: {db_stats.get('sessions', 'N/A')}")
                
                ws_stats = data['websocket']
                print(f"\nWebSocket Statistics:")
                print(f"  Total connections: {ws_stats['total_connections']}")
                
                return True
            else:
                print_error(f"Failed to get stats: {response.status_code}")
                return False
                
        except Exception as e:
            print_error(f"Stats error: {e}")
            return False
    
    def run_all_tests(self):
        """Run all tests in sequence"""
        print_header("GIBSEY MYCELIAL NETWORK API TESTS")
        print(f"Testing API at: {BASE_URL}")
        print(f"Time: {datetime.now().isoformat()}")
        
        tests = [
            ("Health Check", self.test_health),
            ("Get Pages", self.test_get_pages),
            ("Create Page", self.test_create_page),
            ("User & Session", self.test_user_session),
            ("API Statistics", self.test_api_stats)
        ]
        
        results = {}
        
        for test_name, test_func in tests:
            try:
                results[test_name] = test_func()
            except Exception as e:
                print_error(f"Test '{test_name}' crashed: {e}")
                results[test_name] = False
        
        # Run async WebSocket test
        try:
            results["WebSocket"] = asyncio.run(self.test_websocket())
        except Exception as e:
            print_error(f"WebSocket test crashed: {e}")
            results["WebSocket"] = False
        
        # Summary
        print_header("TEST SUMMARY")
        
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        for test_name, result in results.items():
            status = "PASSED" if result else "FAILED"
            color = Colors.GREEN if result else Colors.RED
            print(f"{color}{test_name:.<40} {status}{Colors.END}")
        
        print(f"\nTotal: {passed}/{total} tests passed")
        
        if passed == total:
            print_success("All tests passed! 🎉")
        else:
            print_error("Some tests failed. Check the output above.")
        
        # Cleanup info
        if self.created_resources['pages']:
            print_info(f"Created {len(self.created_resources['pages'])} test pages")
        if self.created_resources['users']:
            print_info(f"Created {len(self.created_resources['users'])} test users")

def main():
    """Main test runner"""
    tester = GibseyAPITester()
    
    # Check if specific test requested
    if len(sys.argv) > 1:
        test_name = sys.argv[1]
        if hasattr(tester, f"test_{test_name}"):
            getattr(tester, f"test_{test_name}")()
        else:
            print_error(f"Unknown test: {test_name}")
            print("Available tests: health, get_pages, create_page, user_session, api_stats, websocket")
    else:
        # Run all tests
        tester.run_all_tests()

if __name__ == "__main__":
    main()