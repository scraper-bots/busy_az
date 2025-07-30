import React, { useState } from 'react';
import { Container, Row, Col, Button } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import ResumeForm from './components/ResumeForm';
import ResumePreview from './components/ResumePreview';
import PaymentForm from './components/PaymentForm';
import TemplateSelector from './components/TemplateSelector';
import './App.css';

function App() {
  const [step, setStep] = useState(1); // 1: template, 2: form, 3: preview, 4: payment
  const [resumeData, setResumeData] = useState({
    personalInfo: {
      fullName: '',
      email: '',
      phone: '',
      address: '',
      linkedin: '',
      website: ''
    },
    experience: [],
    education: [],
    skills: []
  });
  const [selectedTemplate, setSelectedTemplate] = useState(1);

  const handleNext = () => {
    setStep(step + 1);
  };

  const handleBack = () => {
    setStep(step - 1);
  };

  const handleTemplateSelect = (templateId) => {
    setSelectedTemplate(templateId);
    handleNext();
  };

  const handleFormSubmit = (data) => {
    setResumeData(data);
    handleNext();
  };

  const handlePaymentSuccess = () => {
    // In a real app, this would handle the payment success
    alert('Payment successful! Your resume will be downloaded shortly.');
    // Here we would trigger the PDF download
  };

  return (
    <div className="App">
      <header className="App-header py-4 bg-primary text-white">
        <Container>
          <h1 className="text-center">Professional Resume Builder</h1>
          <p className="text-center mb-0">Create your perfect resume in minutes</p>
        </Container>
      </header>

      <Container className="my-5">
        {step === 1 && (
          <TemplateSelector onSelect={handleTemplateSelect} />
        )}

        {step === 2 && (
          <ResumeForm 
            data={resumeData} 
            onSubmit={handleFormSubmit} 
            onBack={handleBack}
          />
        )}

        {step === 3 && (
          <div>
            <Row>
              <Col md={8}>
                <ResumePreview data={resumeData} template={selectedTemplate} />
              </Col>
              <Col md={4}>
                <div className="d-flex flex-column">
                  <Button variant="secondary" onClick={handleBack} className="mb-2">
                    Back to Edit
                  </Button>
                  <Button variant="primary" onClick={handleNext} className="mb-2">
                    Proceed to Payment
                  </Button>
                </div>
              </Col>
            </Row>
          </div>
        )}

        {step === 4 && (
          <PaymentForm 
            onPaymentSuccess={handlePaymentSuccess} 
            onBack={handleBack}
          />
        )}
      </Container>

      <footer className="bg-light py-4 mt-5">
        <Container>
          <p className="text-center mb-0">© {new Date().getFullYear()} Resume Builder. All rights reserved.</p>
        </Container>
      </footer>
    </div>
  );
}

export default App;