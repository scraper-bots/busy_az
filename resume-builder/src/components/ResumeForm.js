import React, { useState, useEffect } from 'react';
import { Form, Button, Row, Col, Card } from 'react-bootstrap';

const ResumeForm = ({ data, onSubmit, onBack }) => {
  const [formData, setFormData] = useState(data);

  useEffect(() => {
    setFormData(data);
  }, [data]);

  const handleChange = (section, field, value, index = null) => {
    setFormData(prev => {
      if (index !== null) {
        // Handle array fields (experience, education)
        const updatedSection = [...prev[section]];
        updatedSection[index] = { ...updatedSection[index], [field]: value };
        return { ...prev, [section]: updatedSection };
      } else if (section === 'personalInfo') {
        // Handle personal info
        return { ...prev, personalInfo: { ...prev.personalInfo, [field]: value } };
      } else {
        // Handle skills
        return { ...prev, [section]: value.split(',').map(skill => skill.trim()) };
      }
    });
  };

  const addExperience = () => {
    setFormData(prev => ({
      ...prev,
      experience: [...prev.experience, { company: '', position: '', startDate: '', endDate: '', description: '' }]
    }));
  };

  const addEducation = () => {
    setFormData(prev => ({
      ...prev,
      education: [...prev.education, { institution: '', degree: '', startDate: '', endDate: '', description: '' }]
    }));
  };

  const removeExperience = (index) => {
    setFormData(prev => {
      const updatedExperience = [...prev.experience];
      updatedExperience.splice(index, 1);
      return { ...prev, experience: updatedExperience };
    });
  };

  const removeEducation = (index) => {
    setFormData(prev => {
      const updatedEducation = [...prev.education];
      updatedEducation.splice(index, 1);
      return { ...prev, education: updatedEducation };
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <Form onSubmit={handleSubmit}>
      <h2 className="text-center mb-4">Create Your Resume</h2>
      
      {/* Personal Information */}
      <Card className="mb-4">
        <Card.Header>Personal Information</Card.Header>
        <Card.Body>
          <Row>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Full Name</Form.Label>
                <Form.Control
                  type="text"
                  value={formData.personalInfo.fullName}
                  onChange={(e) => handleChange('personalInfo', 'fullName', e.target.value)}
                  required
                />
              </Form.Group>
            </Col>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Email</Form.Label>
                <Form.Control
                  type="email"
                  value={formData.personalInfo.email}
                  onChange={(e) => handleChange('personalInfo', 'email', e.target.value)}
                  required
                />
              </Form.Group>
            </Col>
          </Row>
          
          <Row>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Phone</Form.Label>
                <Form.Control
                  type="text"
                  value={formData.personalInfo.phone}
                  onChange={(e) => handleChange('personalInfo', 'phone', e.target.value)}
                />
              </Form.Group>
            </Col>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Address</Form.Label>
                <Form.Control
                  type="text"
                  value={formData.personalInfo.address}
                  onChange={(e) => handleChange('personalInfo', 'address', e.target.value)}
                />
              </Form.Group>
            </Col>
          </Row>
          
          <Row>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>LinkedIn</Form.Label>
                <Form.Control
                  type="text"
                  value={formData.personalInfo.linkedin}
                  onChange={(e) => handleChange('personalInfo', 'linkedin', e.target.value)}
                />
              </Form.Group>
            </Col>
            <Col md={6}>
              <Form.Group className="mb-3">
                <Form.Label>Website</Form.Label>
                <Form.Control
                  type="text"
                  value={formData.personalInfo.website}
                  onChange={(e) => handleChange('personalInfo', 'website', e.target.value)}
                />
              </Form.Group>
            </Col>
          </Row>
        </Card.Body>
      </Card>
      
      {/* Work Experience */}
      <Card className="mb-4">
        <Card.Header>
          Work Experience
          <Button variant="success" size="sm" className="float-end" onClick={addExperience}>
            Add Experience
          </Button>
        </Card.Header>
        <Card.Body>
          {formData.experience.map((exp, index) => (
            <Card key={index} className="mb-3">
              <Card.Body>
                <Row>
                  <Col md={6}>
                    <Form.Group className="mb-3">
                      <Form.Label>Company</Form.Label>
                      <Form.Control
                        type="text"
                        value={exp.company}
                        onChange={(e) => handleChange('experience', 'company', e.target.value, index)}
                        required
                      />
                    </Form.Group>
                  </Col>
                  <Col md={6}>
                    <Form.Group className="mb-3">
                      <Form.Label>Position</Form.Label>
                      <Form.Control
                        type="text"
                        value={exp.position}
                        onChange={(e) => handleChange('experience', 'position', e.target.value, index)}
                        required
                      />
                    </Form.Group>
                  </Col>
                </Row>
                
                <Row>
                  <Col md={6}>
                    <Form.Group className="mb-3">
                      <Form.Label>Start Date</Form.Label>
                      <Form.Control
                        type="text"
                        placeholder="MM/YYYY"
                        value={exp.startDate}
                        onChange={(e) => handleChange('experience', 'startDate', e.target.value, index)}
                      />
                    </Form.Group>
                  </Col>
                  <Col md={6}>
                    <Form.Group className="mb-3">
                      <Form.Label>End Date</Form.Label>
                      <Form.Control
                        type="text"
                        placeholder="MM/YYYY or Present"
                        value={exp.endDate}
                        onChange={(e) => handleChange('experience', 'endDate', e.target.value, index)}
                      />
                    </Form.Group>
                  </Col>
                </Row>
                
                <Form.Group className="mb-3">
                  <Form.Label>Description</Form.Label>
                  <Form.Control
                    as="textarea"
                    rows={3}
                    value={exp.description}
                    onChange={(e) => handleChange('experience', 'description', e.target.value, index)}
                  />
                </Form.Group>
                
                <Button variant="danger" size="sm" onClick={() => removeExperience(index)}>
                  Remove Experience
                </Button>
              </Card.Body>
            </Card>
          ))}
          
          {formData.experience.length === 0 && (
            <p className="text-center text-muted">No work experience added yet</p>
          )}
        </Card.Body>
      </Card>
      
      {/* Education */}
      <Card className="mb-4">
        <Card.Header>
          Education
          <Button variant="success" size="sm" className="float-end" onClick={addEducation}>
            Add Education
          </Button>
        </Card.Header>
        <Card.Body>
          {formData.education.map((edu, index) => (
            <Card key={index} className="mb-3">
              <Card.Body>
                <Row>
                  <Col md={6}>
                    <Form.Group className="mb-3">
                      <Form.Label>Institution</Form.Label>
                      <Form.Control
                        type="text"
                        value={edu.institution}
                        onChange={(e) => handleChange('education', 'institution', e.target.value, index)}
                        required
                      />
                    </Form.Group>
                  </Col>
                  <Col md={6}>
                    <Form.Group className="mb-3">
                      <Form.Label>Degree</Form.Label>
                      <Form.Control
                        type="text"
                        value={edu.degree}
                        onChange={(e) => handleChange('education', 'degree', e.target.value, index)}
                        required
                      />
                    </Form.Group>
                  </Col>
                </Row>
                
                <Row>
                  <Col md={6}>
                    <Form.Group className="mb-3">
                      <Form.Label>Start Date</Form.Label>
                      <Form.Control
                        type="text"
                        placeholder="MM/YYYY"
                        value={edu.startDate}
                        onChange={(e) => handleChange('education', 'startDate', e.target.value, index)}
                      />
                    </Form.Group>
                  </Col>
                  <Col md={6}>
                    <Form.Group className="mb-3">
                      <Form.Label>End Date</Form.Label>
                      <Form.Control
                        type="text"
                        placeholder="MM/YYYY or Present"
                        value={edu.endDate}
                        onChange={(e) => handleChange('education', 'endDate', e.target.value, index)}
                      />
                    </Form.Group>
                  </Col>
                </Row>
                
                <Form.Group className="mb-3">
                  <Form.Label>Description</Form.Label>
                  <Form.Control
                    as="textarea"
                    rows={3}
                    value={edu.description}
                    onChange={(e) => handleChange('education', 'description', e.target.value, index)}
                  />
                </Form.Group>
                
                <Button variant="danger" size="sm" onClick={() => removeEducation(index)}>
                  Remove Education
                </Button>
              </Card.Body>
            </Card>
          ))}
          
          {formData.education.length === 0 && (
            <p className="text-center text-muted">No education added yet</p>
          )}
        </Card.Body>
      </Card>
      
      {/* Skills */}
      <Card className="mb-4">
        <Card.Header>Skills</Card.Header>
        <Card.Body>
          <Form.Group className="mb-3">
            <Form.Label>Skills (comma separated)</Form.Label>
            <Form.Control
              type="text"
              placeholder="e.g., JavaScript, React, Node.js"
              value={formData.skills.join(', ')}
              onChange={(e) => handleChange('skills', null, e.target.value)}
            />
          </Form.Group>
        </Card.Body>
      </Card>
      
      {/* Form Actions */}
      <div className="d-flex justify-content-between">
        <Button variant="secondary" onClick={onBack}>
          Back
        </Button>
        <Button variant="primary" type="submit">
          Preview Resume
        </Button>
      </div>
    </Form>
  );
};

export default ResumeForm;