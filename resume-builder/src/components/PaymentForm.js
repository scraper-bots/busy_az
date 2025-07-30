import React, { useState } from 'react';
import { Form, Button, Row, Col, Card } from 'react-bootstrap';

const PaymentForm = ({ onPaymentSuccess, onBack }) => {
  const [paymentMethod, setPaymentMethod] = useState('credit');
  const [cardInfo, setCardInfo] = useState({
    cardNumber: '',
    expiryDate: '',
    cvv: '',
    name: ''
  });
  const [paypalInfo, setPaypalInfo] = useState({
    email: ''
  });

  const handleCardChange = (e) => {
    const { name, value } = e.target;
    setCardInfo(prev => ({ ...prev, [name]: value }));
  };

  const handlePaypalChange = (e) => {
    const { name, value } = e.target;
    setPaypalInfo(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // In a real app, we would process the payment here
    // For now, we'll just simulate a successful payment
    onPaymentSuccess();
  };

  return (
    <div>
      <h2 className="text-center mb-4">Payment Information</h2>
      <Row className="justify-content-center">
        <Col md={8}>
          <Card className="payment-form">
            <Card.Body>
              <Form onSubmit={handleSubmit}>
                <Form.Group className="mb-3">
                  <Form.Label>Payment Method</Form.Label>
                  <div>
                    <Form.Check
                      inline
                      label="Credit Card"
                      type="radio"
                      name="paymentMethod"
                      id="credit"
                      checked={paymentMethod === 'credit'}
                      onChange={() => setPaymentMethod('credit')}
                    />
                    <Form.Check
                      inline
                      label="PayPal"
                      type="radio"
                      name="paymentMethod"
                      id="paypal"
                      checked={paymentMethod === 'paypal'}
                      onChange={() => setPaymentMethod('paypal')}
                    />
                  </div>
                </Form.Group>

                {paymentMethod === 'credit' ? (
                  <>
                    <Form.Group className="mb-3">
                      <Form.Label>Name on Card</Form.Label>
                      <Form.Control
                        type="text"
                        name="name"
                        value={cardInfo.name}
                        onChange={handleCardChange}
                        required
                      />
                    </Form.Group>
                    <Form.Group className="mb-3">
                      <Form.Label>Card Number</Form.Label>
                      <Form.Control
                        type="text"
                        name="cardNumber"
                        placeholder="1234 5678 9012 3456"
                        value={cardInfo.cardNumber}
                        onChange={handleCardChange}
                        required
                      />
                    </Form.Group>
                    <Row>
                      <Col md={6}>
                        <Form.Group className="mb-3">
                          <Form.Label>Expiry Date</Form.Label>
                          <Form.Control
                            type="text"
                            name="expiryDate"
                            placeholder="MM/YY"
                            value={cardInfo.expiryDate}
                            onChange={handleCardChange}
                            required
                          />
                        </Form.Group>
                      </Col>
                      <Col md={6}>
                        <Form.Group className="mb-3">
                          <Form.Label>CVV</Form.Label>
                          <Form.Control
                            type="text"
                            name="cvv"
                            placeholder="123"
                            value={cardInfo.cvv}
                            onChange={handleCardChange}
                            required
                          />
                        </Form.Group>
                      </Col>
                    </Row>
                  </>
                ) : (
                  <Form.Group className="mb-3">
                    <Form.Label>PayPal Email</Form.Label>
                    <Form.Control
                      type="email"
                      name="email"
                      value={paypalInfo.email}
                      onChange={handlePaypalChange}
                      required
                    />
                  </Form.Group>
                )}

                <div className="d-flex justify-content-between mt-4">
                  <Button variant="secondary" onClick={onBack}>
                    Back
                  </Button>
                  <Button variant="success" type="submit">
                    Pay $19.99
                  </Button>
                </div>
              </Form>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default PaymentForm;