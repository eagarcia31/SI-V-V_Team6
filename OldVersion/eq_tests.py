def test_process_payment():
    # Test for cash payment
    with patch('builtins.input', side_effect=[2.0]):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        process_payment('Coke', 'cash')
        sys.stdout = sys.__stdout__
        assert "Thank you for your purchase!" in captured_output.getvalue()
        assert "Here's your Coke." in captured_output.getvalue()

    # Test for credit payment
    captured_output = io.StringIO()
    sys.stdout = captured_output
    process_payment('Pepsi', 'credit')
    sys.stdout = sys.__stdout__
    assert "Thank you for your purchase!" in captured_output.getvalue()
    assert "Here's your Pepsi." in captured_output.getvalue()

    # Test for invalid payment method
    captured_output = io.StringIO()
    sys.stdout = captured_output
    process_payment('Water', 'paypal')
    sys.stdout = sys.__stdout__
    assert "Sorry, we do not accept that payment method." in captured_output.getvalue()
