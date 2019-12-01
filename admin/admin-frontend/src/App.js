import React from 'react';
import logo from './logo.svg';
import './App.css';
import SubmissionTemplate from './SubmissionTemplate'
import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'

function App() {
  document.body.style = 'background: rgb(70, 70, 102);';
  return (
    <div className="App">
      <Container fluid={"true"} style={{ backgroundColor: "rgb(70, 70, 102)"}}>
      <Row fluid={"true"} >

        {/* idk why, but I had to add empty cols to center my component*/}
        <Col fluid={"true"}></Col>
        <Col fluid={"true"}><SubmissionTemplate /></Col>
        <Col fluid={"true"}></Col>
        
      </Row>
    </Container>
    </div>
  );
}

export default App;
