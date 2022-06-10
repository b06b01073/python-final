import { useState, useEffect, useRef } from "react";
import Search from "./Search";
import { Container, Row, Col, ListGroup, Modal, Button } from "react-bootstrap";

const Landing = () => {
  return (
    <div className="landing-page">
      <Container className="form-container">
        <Row className="justify-content-md-center">
          <Col xs lg="10">
            <Search />
          </Col>
        </Row>
      </Container>
    </div>
  );
};

export default Landing;
