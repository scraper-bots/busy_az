import React from 'react';
import { Row, Col, Card, Button } from 'react-bootstrap';

const TemplateSelector = ({ onSelect }) => {
  const templates = [
    { id: 1, name: 'Classic', description: 'A clean and professional template' },
    { id: 2, name: 'Modern', description: 'A contemporary design with bold elements' },
    { id: 3, name: 'Creative', description: 'A unique layout for creative professionals' }
  ];

  return (
    <div>
      <h2 className="text-center mb-5">Choose a Resume Template</h2>
      <Row>
        {templates.map(template => (
          <Col md={4} key={template.id} className="mb-4">
            <Card className="template-card h-100" onClick={() => onSelect(template.id)}>
              <Card.Body className="d-flex flex-column">
                <Card.Title>{template.name}</Card.Title>
                <Card.Text>{template.description}</Card.Text>
                <Button variant="primary" className="mt-auto">Select</Button>
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>
    </div>
  );
};

export default TemplateSelector;