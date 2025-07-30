import React from 'react';
import { Document, Page, Text, View, StyleSheet, Font } from '@react-pdf/renderer';

// Register font
Font.register({
  family: 'Roboto',
  src: 'https://cdnjs.cloudflare.com/ajax/libs/ink/3.1.10/fonts/Roboto/roboto-light-webfont.ttf',
  fontWeight: 'normal'
});

// Create styles
const styles = StyleSheet.create({
  page: {
    padding: 30,
    fontFamily: 'Roboto'
  },
  header: {
    marginBottom: 20,
    paddingBottom: 10,
    borderBottomWidth: 1,
    borderBottomColor: '#000',
    borderBottomStyle: 'solid'
  },
  name: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 5
  },
  contactInfo: {
    fontSize: 10,
    marginBottom: 2
  },
  section: {
    marginBottom: 15
  },
  sectionTitle: {
    fontSize: 14,
    fontWeight: 'bold',
    marginBottom: 8,
    textTransform: 'uppercase'
  },
  experienceItem: {
    marginBottom: 10
  },
  experienceHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 3
  },
  experienceTitle: {
    fontSize: 12,
    fontWeight: 'bold'
  },
  experienceCompany: {
    fontSize: 11
  },
  experienceDate: {
    fontSize: 10
  },
  experienceDescription: {
    fontSize: 10,
    marginBottom: 5
  },
  educationItem: {
    marginBottom: 10
  },
  educationHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 3
  },
  educationTitle: {
    fontSize: 12,
    fontWeight: 'bold'
  },
  educationInstitution: {
    fontSize: 11
  },
  educationDate: {
    fontSize: 10
  },
  skillsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap'
  },
  skill: {
    fontSize: 10,
    marginRight: 10,
    marginBottom: 5
  }
});

// Create Document Component
const ResumeDocument = ({ data }) => {
  return (
    <Document>
      <Page size="A4" style={styles.page}>
        {/* Header with personal info */}
        <View style={styles.header}>
          <Text style={styles.name}>{data.personalInfo.fullName}</Text>
          <Text style={styles.contactInfo}>{data.personalInfo.email} | {data.personalInfo.phone}</Text>
          {data.personalInfo.address && <Text style={styles.contactInfo}>{data.personalInfo.address}</Text>}
          <View style={{ flexDirection: 'row' }}>
            {data.personalInfo.linkedin && <Text style={styles.contactInfo}>LinkedIn: {data.personalInfo.linkedin} </Text>}
            {data.personalInfo.website && <Text style={styles.contactInfo}>Website: {data.personalInfo.website}</Text>}
          </View>
        </View>

        {/* Work Experience */}
        {data.experience.length > 0 && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Work Experience</Text>
            {data.experience.map((exp, index) => (
              <View key={index} style={styles.experienceItem}>
                <View style={styles.experienceHeader}>
                  <Text style={styles.experienceTitle}>{exp.position}</Text>
                  <Text style={styles.experienceDate}>
                    {exp.startDate} - {exp.endDate}
                  </Text>
                </View>
                <Text style={styles.experienceCompany}>{exp.company}</Text>
                <Text style={styles.experienceDescription}>{exp.description}</Text>
              </View>
            ))}
          </View>
        )}

        {/* Education */}
        {data.education.length > 0 && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Education</Text>
            {data.education.map((edu, index) => (
              <View key={index} style={styles.educationItem}>
                <View style={styles.educationHeader}>
                  <Text style={styles.educationTitle}>{edu.degree}</Text>
                  <Text style={styles.educationDate}>
                    {edu.startDate} - {edu.endDate}
                  </Text>
                </View>
                <Text style={styles.educationInstitution}>{edu.institution}</Text>
                <Text style={styles.experienceDescription}>{edu.description}</Text>
              </View>
            ))}
          </View>
        )}

        {/* Skills */}
        {data.skills.length > 0 && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Skills</Text>
            <View style={styles.skillsContainer}>
              {data.skills.map((skill, index) => (
                <Text key={index} style={styles.skill}>{skill}</Text>
              ))}
            </View>
          </View>
        )}
      </Page>
    </Document>
  );
};

// Web Preview Component
const ResumePreview = ({ data }) => {
  return (
    <div className="resume-preview">
      <h3 className="text-center mb-4">Resume Preview</h3>
      <div className="p-4 bg-white border">
        <div className="mb-4 pb-3 border-bottom">
          <h2 className="mb-2">{data.personalInfo.fullName}</h2>
          <p className="mb-1">
            <strong>Email:</strong> {data.personalInfo.email}
          </p>
          {data.personalInfo.phone && (
            <p className="mb-1">
              <strong>Phone:</strong> {data.personalInfo.phone}
            </p>
          )}
          {data.personalInfo.address && (
            <p className="mb-1">
              <strong>Address:</strong> {data.personalInfo.address}
            </p>
          )}
          <div>
            {data.personalInfo.linkedin && (
              <span className="me-3">
                <strong>LinkedIn:</strong> {data.personalInfo.linkedin}
              </span>
            )}
            {data.personalInfo.website && (
              <span>
                <strong>Website:</strong> {data.personalInfo.website}
              </span>
            )}
          </div>
        </div>

        {data.experience.length > 0 && (
          <div className="mb-4">
            <h4 className="border-bottom pb-2 mb-3">Work Experience</h4>
            {data.experience.map((exp, index) => (
              <div key={index} className="mb-3">
                <div className="d-flex justify-content-between">
                  <h5 className="mb-1">{exp.position}</h5>
                  <span>
                    {exp.startDate} - {exp.endDate}
                  </span>
                </div>
                <p className="mb-1 fw-bold">{exp.company}</p>
                <p className="mb-0">{exp.description}</p>
              </div>
            ))}
          </div>
        )}

        {data.education.length > 0 && (
          <div className="mb-4">
            <h4 className="border-bottom pb-2 mb-3">Education</h4>
            {data.education.map((edu, index) => (
              <div key={index} className="mb-3">
                <div className="d-flex justify-content-between">
                  <h5 className="mb-1">{edu.degree}</h5>
                  <span>
                    {edu.startDate} - {edu.endDate}
                  </span>
                </div>
                <p className="mb-1 fw-bold">{edu.institution}</p>
                <p className="mb-0">{edu.description}</p>
              </div>
            ))}
          </div>
        )}

        {data.skills.length > 0 && (
          <div>
            <h4 className="border-bottom pb-2 mb-3">Skills</h4>
            <div>
              {data.skills.map((skill, index) => (
                <span key={index} className="badge bg-secondary me-2 mb-2">
                  {skill}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export { ResumeDocument };
export default ResumePreview;