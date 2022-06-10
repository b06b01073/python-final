import React from "react";

import { Navbar, Nav as N, Container } from "react-bootstrap";

const Nav = () => {
  return (
    <>
      <Navbar bg="dark" variant="dark">
        <Container>
          <Navbar.Brand href="#home">Group 1</Navbar.Brand>
          <N className="me-rl">
            <N.Link
              href="https://github.com/b06b01073/python-final-project"
              target="_blank"
            >
              Github
            </N.Link>
          </N>
        </Container>
      </Navbar>
    </>
  );
};

export default Nav;
