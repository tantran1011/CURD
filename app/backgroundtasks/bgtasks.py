def send_email_confirmation(email: str, order_id: str, body:list = []):
    # Simulate sending an email
    print(f"Sending email to {email}")
    x = f"""
    Dear Customer,
    Thank you for your order #{order_id}.
    Your order details are as follows:
    {body}
    """
    print(x)