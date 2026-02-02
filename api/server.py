from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import base64
import sys
import os
from urllib.parse import urlparse, parse_qs

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from dsa.xml_parser import parse_xml_to_json

# ============================================================================
# GLOBAL CONFIGURATION
# ============================================================================

# In-memory data storage
transactions = []
next_id = 1

# Authentication credentials
# WARNING: Hardcoding credentials is INSECURE!
# In production, use environment variables and hashed passwords
VALID_USERNAME = "admin"
VALID_PASSWORD = "password123"


# ============================================================================
# API REQUEST HANDLER
# ============================================================================

class TransactionAPIHandler(BaseHTTPRequestHandler):
    """
    Handles HTTP requests for the Transaction API.
    
    Methods:
        do_GET: Handle GET requests
        do_POST: Handle POST requests
        do_PUT: Handle PUT requests
        do_DELETE: Handle DELETE requests
    """
    
    def log_message(self, format, *args):
        """
        Override to add colored logging.
        """
        method = args[0].split()[0] if args else ''
        
        color_codes = {
            'GET': '\033[92m',      # Green
            'POST': '\033[94m',     # Blue
            'PUT': '\033[93m',      # Yellow
            'DELETE': '\033[91m',   # Red
        }
        
        color = color_codes.get(method, '\033[0m')
        reset = '\033[0m'
        
        print(f"{color}[{self.log_date_time_string()}] {format % args}{reset}")
    
    def do_AUTHHEAD(self):
        """
        Send authentication challenge to client.
        Called when authentication fails.
        """
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm="Transaction API"')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
    
    def check_authentication(self):
        """
        Verify Basic Authentication credentials.
        
        Basic Auth Process:
            1. Client sends: Authorization: Basic <base64(username:password)>
            2. Server decodes the base64 string
            3. Server checks if credentials match
        
        Returns:
            bool: True if authenticated, False otherwise
            
        Security Note:
            Basic Auth sends credentials in base64 (NOT encrypted!)
            This can be decoded easily. Always use HTTPS in production.
        """
        auth_header = self.headers.get('Authorization')
        
        if auth_header is None:
            return False
        
        try:
            # Split "Basic" and the encoded credentials
            auth_type, auth_string = auth_header.split(' ', 1)
            
            if auth_type.lower() != 'basic':
                return False
            
            # Decode base64
            decoded_bytes = base64.b64decode(auth_string)
            decoded_string = decoded_bytes.decode('utf-8')
            
            # Split username and password
            username, password = decoded_string.split(':', 1)
            
            # Verify credentials
            return username == VALID_USERNAME and password == VALID_PASSWORD
            
        except Exception as e:
            print(f"Authentication error: {e}")
            return False
    
    def send_json_response(self, data, status_code=200):
        """
        Helper method to send JSON response.
        
        Args:
            data: Dictionary or list to send as JSON
            status_code: HTTP status code (default 200)
        """
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')  # CORS
        self.end_headers()
        
        response_json = json.dumps(data, indent=2, ensure_ascii=False)
        self.wfile.write(response_json.encode('utf-8'))
    
    def parse_path(self):
        """
        Parse the URL path to extract resource information.
        
        Examples:
            /transactions → ('/transactions', None)
            /transactions/5 → ('/transactions', 5)
            /transactions?type=payment → ('/transactions', None, {'type': ['payment']})
        
        Returns:
            tuple: (base_path, resource_id, query_params)
        """
        parsed = urlparse(self.path)
        path_parts = parsed.path.strip('/').split('/')
        
        base_path = '/' + path_parts[0] if path_parts else '/'
        
        # Extract resource ID if present
        resource_id = None
        if len(path_parts) > 1 and path_parts[1].isdigit():
            resource_id = int(path_parts[1])
        
        # Parse query parameters
        query_params = parse_qs(parsed.query)
        
        return base_path, resource_id, query_params
    
    def filter_transactions(self, transactions, query_params):
        """
        Filter transactions based on query parameters.
        
        Supported filters:
            ?type=payment
            ?amount_min=1000
            ?amount_max=5000
            ?sender=Jane
            ?recipient=John
        
        Args:
            transactions: List of transactions
            query_params: Dictionary of query parameters
            
        Returns:
            list: Filtered transactions
        """
        filtered = transactions
        
        # Filter by type
        if 'type' in query_params:
            trans_type = query_params['type'][0]
            filtered = [t for t in filtered if t.get('type') == trans_type]
        
        # Filter by amount range
        if 'amount_min' in query_params:
            min_amount = int(query_params['amount_min'][0])
            filtered = [t for t in filtered if t.get('amount', 0) >= min_amount]
        
        if 'amount_max' in query_params:
            max_amount = int(query_params['amount_max'][0])
            filtered = [t for t in filtered if t.get('amount', 0) <= max_amount]
        
        # Filter by sender
        if 'sender' in query_params:
            sender = query_params['sender'][0].lower()
            filtered = [t for t in filtered 
                       if t.get('sender') and sender in t['sender'].lower()]
        
        # Filter by recipient
        if 'recipient' in query_params:
            recipient = query_params['recipient'][0].lower()
            filtered = [t for t in filtered 
                       if t.get('recipient') and recipient in t['recipient'].lower()]
        
        return filtered
    
    # ========================================================================
    # HTTP METHOD HANDLERS
    # ========================================================================
    
    def do_GET(self):
        """
        Handle GET requests.
        
        Endpoints:
            GET /transactions → List all (with optional filters)
            GET /transactions/{id} → Get specific transaction
        """
        # Check authentication
        if not self.check_authentication():
            self.do_AUTHHEAD()
            self.wfile.write(json.dumps({
                'error': 'Unauthorized',
                'message': 'Valid credentials required. Use username: admin, password: password123'
            }).encode())
            return
        
        base_path, resource_id, query_params = self.parse_path()
        
        # Validate endpoint
        if base_path != '/transactions':
            self.send_json_response({
                'error': 'Not Found',
                'message': f'Endpoint {base_path} does not exist'
            }, 404)
            return
        
        # GET /transactions/{id} - Get specific transaction
        if resource_id is not None:
            transaction = next((t for t in transactions if t['id'] == resource_id), None)
            
            if transaction:
                self.send_json_response({
                    'success': True,
                    'transaction': transaction
                })
            else:
                self.send_json_response({
                    'error': 'Not Found',
                    'message': f'Transaction with ID {resource_id} does not exist'
                }, 404)
        
        # GET /transactions - List all (with optional filters)
        else:
            filtered = self.filter_transactions(transactions, query_params)
            
            self.send_json_response({
                'success': True,
                'count': len(filtered),
                'total': len(transactions),
                'filters': query_params if query_params else None,
                'transactions': filtered
            })
    
    def do_POST(self):
        """
        Handle POST requests (Create new transaction).
        
        Endpoint:
            POST /transactions
        
        Request Body:
            {
                "type": "payment",
                "amount": 5000,
                "recipient": "John Doe",
                "fee": 100
            }
        """
        # Check authentication
        if not self.check_authentication():
            self.do_AUTHHEAD()
            self.wfile.write(json.dumps({'error': 'Unauthorized'}).encode())
            return
        
        base_path, _, _ = self.parse_path()
        
        if base_path != '/transactions':
            self.send_json_response({'error': 'Not Found'}, 404)
            return
        
        # Read request body
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length == 0:
            self.send_json_response({
                'error': 'Bad Request',
                'message': 'Request body is required'
            }, 400)
            return
        
        body = self.rfile.read(content_length).decode('utf-8')
        
        try:
            new_transaction = json.loads(body)
            
            # Validate required fields
            if 'type' not in new_transaction:
                self.send_json_response({
                    'error': 'Bad Request',
                    'message': 'Field "type" is required'
                }, 400)
                return
            
            # Assign new ID
            global next_id
            new_transaction['id'] = next_id
            next_id += 1
            
            # Add timestamp
            from datetime import datetime
            new_transaction['created_at'] = datetime.now().isoformat()
            
            # Add to storage
            transactions.append(new_transaction)
            
            self.send_json_response({
                'success': True,
                'message': 'Transaction created successfully',
                'transaction': new_transaction
            }, 201)
            
        except json.JSONDecodeError:
            self.send_json_response({
                'error': 'Bad Request',
                'message': 'Invalid JSON in request body'
            }, 400)
        except Exception as e:
            self.send_json_response({
                'error': 'Internal Server Error',
                'message': str(e)
            }, 500)
    
    def do_PUT(self):
        """
        Handle PUT requests (Update existing transaction).
        
        Endpoint:
            PUT /transactions/{id}
        
        Request Body:
            {
                "amount": 7500,
                "fee": 150
            }
        """
        # Check authentication
        if not self.check_authentication():
            self.do_AUTHHEAD()
            self.wfile.write(json.dumps({'error': 'Unauthorized'}).encode())
            return
        
        base_path, resource_id, _ = self.parse_path()
        
        if base_path != '/transactions' or resource_id is None:
            self.send_json_response({
                'error': 'Bad Request',
                'message': 'Transaction ID is required in URL'
            }, 400)
            return
        
        # Find existing transaction
        transaction = next((t for t in transactions if t['id'] == resource_id), None)
        
        if not transaction:
            self.send_json_response({
                'error': 'Not Found',
                'message': f'Transaction {resource_id} does not exist'
            }, 404)
            return
        
        # Read update data
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length == 0:
            self.send_json_response({
                'error': 'Bad Request',
                'message': 'Request body is required'
            }, 400)
            return
        
        body = self.rfile.read(content_length).decode('utf-8')
        
        try:
            update_data = json.loads(body)
            
            # Update fields (preserve ID)
            for key, value in update_data.items():
                if key != 'id':  # Never allow ID change
                    transaction[key] = value
            
            # Add update timestamp
            from datetime import datetime
            transaction['updated_at'] = datetime.now().isoformat()
            
            self.send_json_response({
                'success': True,
                'message': 'Transaction updated successfully',
                'transaction': transaction
            })
            
        except json.JSONDecodeError:
            self.send_json_response({
                'error': 'Bad Request',
                'message': 'Invalid JSON'
            }, 400)
    
    def do_DELETE(self):
        """
        Handle DELETE requests.
        
        Endpoint:
            DELETE /transactions/{id}
        """
        # Check authentication
        if not self.check_authentication():
            self.do_AUTHHEAD()
            self.wfile.write(json.dumps({'error': 'Unauthorized'}).encode())
            return
        
        base_path, resource_id, _ = self.parse_path()
        
        if base_path != '/transactions' or resource_id is None:
            self.send_json_response({
                'error': 'Bad Request',
                'message': 'Transaction ID is required'
            }, 400)
            return
        
        # Find and remove
        global transactions
        initial_count = len(transactions)
        transactions = [t for t in transactions if t['id'] != resource_id]
        
        if len(transactions) < initial_count:
            self.send_json_response({
                'success': True,
                'message': f'Transaction {resource_id} deleted successfully'
            })
        else:
            self.send_json_response({
                'error': 'Not Found',
                'message': f'Transaction {resource_id} not found'
            }, 404)
    
    def do_OPTIONS(self):
        """
        Handle OPTIONS requests (for CORS preflight).
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()


# ============================================================================
# SERVER STARTUP
# ============================================================================

def print_banner():
    """
    Print a nice banner when server starts.
    """
    banner = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║         MOBILE MONEY TRANSACTION API SERVER                  ║
    ║         REST API with Basic Authentication                   ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def run_server(port=8000, xml_file=None):
    """
    Initialize and start the API server.
    
    Args:
        port (int): Port number to run server on
        xml_file (str): Path to XML file with transaction data
    """
    global transactions, next_id
    
    print_banner()
    
    # Load data from XML if provided
    if xml_file and os.path.exists(xml_file):
        print(f"Loading data from: {xml_file}")
        transactions = parse_xml_to_json(xml_file)
        next_id = len(transactions) + 1
        print(f"Loaded {len(transactions)} transactions\n")
    else:
        print("No XML file provided. Starting with empty database.\n")
        transactions = []
        next_id = 1
    
    # Server configuration
    server_address = ('', port)
    httpd = HTTPServer(server_address, TransactionAPIHandler)
    
    # Print server information
    print("="*65)
    print("SERVER INFORMATION")
    print("="*65)
    print(f"   Address:        http://localhost:{port}")
    print(f"   Status:         Running")
    print(f"   Transactions:   {len(transactions)}")
    print("="*65)
    print("\nAVAILABLE ENDPOINTS")
    print("="*65)
    print("   GET    /transactions          List all transactions")
    print("   GET    /transactions/{id}     Get specific transaction")
    print("   POST   /transactions          Create new transaction")
    print("   PUT    /transactions/{id}     Update transaction")
    print("   DELETE /transactions/{id}     Delete transaction")
    print("="*65)
    print("\nAUTHENTICATION")
    print("="*65)
    print(f"   Username:  {VALID_USERNAME}")
    print(f"   Password:  {VALID_PASSWORD}")
    print("="*65)
    print("\nEXAMPLE USAGE")
    print("="*65)
    print(f"   curl -u {VALID_USERNAME}:{VALID_PASSWORD} http://localhost:{port}/transactions")
    print("="*65)
    print("\nPress Ctrl+C to stop the server\n")
    
    # Start serving
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\nShutting down server...")
        httpd.shutdown()
        print("Server stopped successfully\n")


if __name__ == '__main__':
    # Get XML file path from command line arguments
    xml_path = None
    port = 8000
    
    if len(sys.argv) > 1:
        xml_path = sys.argv[1]
    
    if len(sys.argv) > 2:
        try:
            port = int(sys.argv[2])
        except ValueError:
            print("Invalid port number. Using default port 8000.")
    
    run_server(port=port, xml_file=xml_path)

