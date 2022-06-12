import { useState } from "react";
import {
  InputGroup,
  FormControl,
  Form,
  Button,
  Modal,
  Row,
  Col,
  Container,
  ButtonGroup,
  Accordion,
} from "react-bootstrap";
import { Send, Funnel, GeoAlt } from "react-bootstrap-icons";
import { useNavigate } from "react-router-dom";

const serverURL = "http://localhost:5000/search";

const redListCategory = [
  // "EX - Extinct",
  // "EW - Extinct In The Wild",
  "CR - Critically Endangered",
  "EN - Endangered",
  "VU - Vulnerable",
  "LR/cd - Lower Risk: Conservation Dependent",
  "NT or LR/nt - Near Threatened",
  // "LC or LR/lc - Least Concern",
  // "DD - Data Deficient",
];
const defaultRadius = 50;

const Search = () => {
  const emptyFilter = {
    family: "",
    genus: "",
  };

  const navigate = useNavigate();

  const [showModal, setShowModal] = useState(false);
  const [filterProps, setFilterProps] = useState(emptyFilter);

  const [tempFilterProps, setTempFilterProps] = useState(emptyFilter);
  const [tempRadius, setTempRadius] = useState(defaultRadius);
  const [radius, setRadius] = useState(defaultRadius);

  const [longitude, setLongitude] = useState("");
  const [latitude, setLatitude] = useState("");

  const [checkedState, setCheckedState] = useState(
    new Array(redListCategory.length).fill(false)
  );
  const [tempCheckedState, setTempCheckedState] = useState(
    new Array(redListCategory.length).fill(false)
  );

  const onSetTempFilterFamily = (e) => {
    setTempFilterProps({ ...tempFilterProps, family: e.target.value });
  };

  const onSetTempFilterGenus = (e) => {
    setTempFilterProps({ ...tempFilterProps, genus: e.target.value });
  };

  const onSetTempRadius = (e) => {
    setTempRadius(e.target.value);
  };

  const changeLatitudeHandler = (e) => {
    setLatitude(e.target.value);
  };

  const changeLongitudeHandler = (e) => {
    setLongitude(e.target.value);
  };

  const getCurrentCoords = () => {
    navigator.geolocation.getCurrentPosition((position) => {
      setLatitude(position.coords.latitude);
      setLongitude(position.coords.longitude);
    });
  };

  const handleCloseWithoutSave = () => {
    setShowModal(false);
  };

  const handleCloseWithSave = () => {
    setShowModal(false);
    setFilterProps(tempFilterProps);
    setCheckedState(tempCheckedState);

    if (tempRadius !== "" && !isNaN(Number(tempRadius))) setRadius(tempRadius);
  };

  const onSetShowModal = () => {
    setShowModal(true);
    setTempFilterProps(filterProps);
    setTempRadius(radius);
    setTempCheckedState(checkedState);
  };

  const coordChecker = (latitude, longitude) => {
    if (latitude === "" || longitude === "") return false;

    latitude = Number(latitude);
    longitude = Number(longitude);

    if (isNaN(latitude) || isNaN(longitude)) {
      return false;
    }

    return true;
  };

  const checkHandler = (position) => {
    const updatedTempCheckedState = tempCheckedState.map((state, index) =>
      index === position ? !state : state
    );

    setTempCheckedState(updatedTempCheckedState);
  };

  const submitHandler = (e) => {
    if (!coordChecker(latitude, longitude)) {
      return;
    }

    const categoryList = {};
    for (let i = 0; i < redListCategory.length; i++) {
      categoryList[redListCategory[i].slice(0, 2)] = checkedState[i];
    }

    const postData = {
      latitude: latitude,
      longitude: longitude,
      radius: Number(radius),
      filter: {
        category: categoryList,
      },
    };

    fetch(serverURL, {
      headers: {
        "Content-Type": "text/plain",
      },
      body: JSON.stringify(postData),
      method: "POST",
    })
      .then((res) => {
        return res.json();
      })
      .then((data) => navigate("/list", { state: data }));
  };

  const checkListJSX = redListCategory.map((type, index) => {
    return (
      <Form.Check
        key={index}
        value={type.slice(0, 2)}
        type="checkbox"
        id={type}
        label={type}
        onChange={() => checkHandler(index)}
        checked={tempCheckedState[index]}
      />
    );
  });

  const style = { textAlign: "center" };

  return (
    <>
      <Modal centered show={showModal}>
        <Modal.Header closeButton onClick={handleCloseWithoutSave}>
          <Modal.Title>Filter</Modal.Title>
        </Modal.Header>

        <Modal.Body>
          <Accordion>
            <Accordion.Item eventKey="1">
              <Accordion.Header>Red List Category</Accordion.Header>
              <Accordion.Body>
                <Form>{checkListJSX}</Form>
              </Accordion.Body>
            </Accordion.Item>
          </Accordion>
        </Modal.Body>

        <Modal.Footer>
          <Button variant="secondary" onClick={handleCloseWithoutSave}>
            Close
          </Button>
          <Button variant="primary" onClick={handleCloseWithSave}>
            Save changes
          </Button>
        </Modal.Footer>
      </Modal>

      <Form>
        <InputGroup size="lg">
          <InputGroup.Text id="inputGroup-sizing-lg">Latitude</InputGroup.Text>
          <FormControl
            aria-label="Large"
            aria-describedby="inputGroup-sizing-sm"
            value={latitude}
            onChange={changeLatitudeHandler}
          />
        </InputGroup>
        <br />
        <InputGroup size="lg">
          <InputGroup.Text id="inputGroup-sizing-lg">Longitude</InputGroup.Text>
          <FormControl
            aria-label="Large"
            aria-describedby="inputGroup-sizing-sm"
            value={longitude}
            onChange={changeLongitudeHandler}
          />
        </InputGroup>

        <br />
        <Container>
          <Row className="justify-content-center" style={style}>
            <Col lg={10}>
              <ButtonGroup aria-label="Basic example">
                <Button variant="primary" size="lg" onClick={getCurrentCoords}>
                  <GeoAlt />
                  Use My Current Location
                </Button>
                <Button variant="success" size="lg" onClick={onSetShowModal}>
                  <Funnel />
                  Filter
                </Button>
                <Button variant="dark" size="lg" onClick={submitHandler}>
                  <Send />
                  Submit
                </Button>
              </ButtonGroup>
            </Col>
          </Row>
        </Container>
      </Form>
    </>
  );
};

export default Search;
