import argparse

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Transport Management System")
    parser.add_argument("--host", required=True, help="Database host")
    parser.add_argument("--user", required=True, help="Database user")
    parser.add_argument("--password", required=True, help="Database password")

    args = parser.parse_args()
    host = args.host
    user = args.user
    password = args.password
    print(f"Host: {host}, User: {user}, Password: {password}")

    # Additional functionality can be added here

if __name__ == "__main__":
    main()
