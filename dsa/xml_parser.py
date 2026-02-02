import xml.etree.ElementTree as ET
import re
import json
from datetime import datetime


def parse_sms_body(body):
    """
    Extract transaction details from SMS message body.
    
    Args:
        body (str): SMS message text
        
    Returns:
        dict: Extracted transaction details
        
    Transaction Types Detected:
        - received: Money received from someone
        - payment: Payment to merchant/person
        - transfer: Direct transfer to another account
        - deposit: Bank deposit to mobile money
        - airtime: Airtime purchase
    """
    details = {
        'transaction_id': None,
        'amount': None,
        'recipient': None,
        'sender': None,
        'type': None,
        'fee': None,
        'new_balance': None,
        'phone_number': None
    }
    
    # Extract Transaction ID (multiple patterns)
    # Pattern 1: "TxId: 73214484437" or "TxId:73214484437"
    txid_match = re.search(r'TxId:?\s*(\d+)', body)
    if txid_match:
        details['transaction_id'] = txid_match.group(1)
    
    # Pattern 2: "Financial Transaction Id: 76662021700"
    fin_txid = re.search(r'Financial Transaction Id:\s*(\d+)', body)
    if fin_txid:
        details['transaction_id'] = fin_txid.group(1)
    
    # Extract Amount (handles both "2000" and "2,000" formats)
    amount_match = re.search(r'(\d+(?:,\d+)*)\s*RWF', body)
    if amount_match:
        # Remove commas and convert to integer
        details['amount'] = int(amount_match.group(1).replace(',', ''))
    
    # Determine transaction type and extract relevant parties
    if 'received' in body.lower():
        details['type'] = 'received'
        # Extract sender name: "from Jane Smith (*********013)"
        sender_match = re.search(r'from\s+([A-Za-z\s]+)\s*\(', body)
        if sender_match:
            details['sender'] = sender_match.group(1).strip()
        
        # Extract partial phone number
        phone_match = re.search(r'\(\*+(\d+)\)', body)
        if phone_match:
            details['phone_number'] = '*' * 9 + phone_match.group(1)
    
    elif 'payment' in body.lower():
        if 'Airtime' in body or 'airtime' in body:
            details['type'] = 'airtime'
            details['recipient'] = 'Airtime'
        else:
            details['type'] = 'payment'
            # Extract recipient: "to Jane Smith 12845"
            recipient_match = re.search(r'to\s+([A-Za-z\s]+)\s+\d+', body)
            if recipient_match:
                details['recipient'] = recipient_match.group(1).strip()
    
    elif 'transferred to' in body.lower():
        details['type'] = 'transfer'
        # Extract recipient and phone: "transferred to Samuel Carter (250791666666)"
        recipient_match = re.search(r'transferred to\s+([A-Za-z\s]+)\s*\((\d+)\)', body)
        if recipient_match:
            details['recipient'] = recipient_match.group(1).strip()
            details['phone_number'] = recipient_match.group(2)
    
    elif 'deposit' in body.lower():
        details['type'] = 'deposit'
        details['recipient'] = 'Bank Account'
    
    else:
        details['type'] = 'unknown'
    
    # Extract Fee (can be 0 or positive amount)
    fee_match = re.search(r'Fee was:?\s*(\d+(?:,\d+)*)\s*RWF', body, re.IGNORECASE)
    if fee_match:
        details['fee'] = int(fee_match.group(1).replace(',', ''))
    
    # Extract New Balance
    balance_match = re.search(r'(?:new balance|NEW BALANCE)\s*:?\s*(\d+(?:,\d+)*)\s*RWF', body, re.IGNORECASE)
    if balance_match:
        details['new_balance'] = int(balance_match.group(1).replace(',', ''))
    
    return details


def parse_xml_to_json(xml_file_path):
    """
    Parse XML file and convert to JSON-compatible list of transactions.
    
    Args:
        xml_file_path (str): Path to XML file
        
    Returns:
        list: List of transaction dictionaries
        
    Example:
        transactions = parse_xml_to_json('modified_sms_v2.xml')
        print(f"Loaded {len(transactions)} transactions")
    """
    try:
        # Parse the XML file
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        
        print(f"Parsing XML file: {xml_file_path}")
        print(f"Total SMS messages found: {root.get('count', 'unknown')}")
        
        transactions = []
        transaction_id = 1
        
        # Iterate through each SMS element
        for sms in root.findall('sms'):
            # Get basic attributes
            body = sms.get('body', '')
            date_timestamp = sms.get('date', '')
            readable_date = sms.get('readable_date', '')
            
            # Skip empty messages
            if not body:
                continue
            
            # Parse the SMS body for transaction details
            details = parse_sms_body(body)
            
            # Create structured transaction object
            transaction = {
                'id': transaction_id,
                'transaction_id': details['transaction_id'],
                'type': details['type'],
                'amount': details['amount'],
                'sender': details['sender'],
                'recipient': details['recipient'],
                'phone_number': details['phone_number'],
                'fee': details['fee'],
                'new_balance': details['new_balance'],
                'timestamp': date_timestamp,
                'readable_date': readable_date,
                'raw_message': body
            }
            
            transactions.append(transaction)
            transaction_id += 1
        
        print(f"Successfully parsed {len(transactions)} transactions")
        return transactions
        
    except FileNotFoundError:
        print(f"Error: File not found - {xml_file_path}")
        return []
    except ET.ParseError as e:
        print(f"Error: Invalid XML format - {e}")
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []


def save_to_json(transactions, output_file='transactions.json'):
    """
    Save parsed transactions to JSON file.
    
    Args:
        transactions (list): List of transaction dictionaries
        output_file (str): Output JSON file path
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(transactions, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(transactions)} transactions to {output_file}")
    except Exception as e:
        print(f"Error saving to JSON: {e}")


def print_transaction_summary(transactions):
    """
    Print summary statistics of parsed transactions.
    
    Args:
        transactions (list): List of transaction dictionaries
    """
    if not transactions:
        print("No transactions to summarize")
        return
    
    # Count by type
    type_counts = {}
    total_amount = 0
    total_fees = 0
    
    for trans in transactions:
        trans_type = trans.get('type', 'unknown')
        type_counts[trans_type] = type_counts.get(trans_type, 0) + 1
        
        if trans.get('amount'):
            total_amount += trans['amount']
        if trans.get('fee'):
            total_fees += trans['fee']
    
    print("\n" + "="*60)
    print("TRANSACTION SUMMARY")
    print("="*60)
    print(f"Total Transactions: {len(transactions)}")
    print(f"\nBreakdown by Type:")
    for trans_type, count in sorted(type_counts.items()):
        print(f"  {trans_type.capitalize()}: {count}")
    print(f"\nTotal Amount Transacted: {total_amount:,} RWF")
    print(f"Total Fees Paid: {total_fees:,} RWF")
    print("="*60 + "\n")


# Example usage
if __name__ == '__main__':
    # Parse XML file
    xml_file = '../modified_sms_v2.xml'  # Adjust path as needed
    transactions = parse_xml_to_json(xml_file)
    
    # Print summary
    print_transaction_summary(transactions)
    
    # Show first few transactions
    print("Sample Transactions (first 3):")
    for trans in transactions[:3]:
        print(json.dumps(trans, indent=2))
        print("-" * 40)
    
    # Save to JSON
    save_to_json(transactions, 'parsed_transactions.json')
