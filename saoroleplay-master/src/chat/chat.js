import React from 'react';

import Navbar from 'react-bootstrap/Navbar';

import DropdownButton from 'react-bootstrap/DropdownButton'

import Dropdown from 'react-bootstrap/Dropdown'

import axios from 'axios'

import './../App.css';

import Button from 'react-bootstrap/Button'

class chat extends React.Component {
    constructor (props) {
    super(props)
    this.state = {

    }
    }

    submitButton = () => {

        return <Button variant = 'dark' disabled> Add Item </Button>
    }

  render() {

    
  return (



    <div>
  <Navbar bg="dark" variant="dark">

<DropdownButton variant = 'dark' id="dropdown-basic-button" title="Dropdown button">
  <Dropdown.Item href="#/action-1">Action</Dropdown.Item>
  <Dropdown.Item href="#/action-2">Another action</Dropdown.Item>
  <Dropdown.Item href="#/action-3">Something else</Dropdown.Item>
</DropdownButton>

  </Navbar>


  <div className = 'characterInfo'>


      <p>Character Name: </p>
      <p>Color of Player: </p>
      <button className='skills' onClick={this.handleMouseDown}>Skills: </button>
      <p className='Inventory'>Inventory: </p>
      <p className='stats'>Stats: </p>


      <form>
          <input type='text'></input>
          {this.submitButton()}
      </form>

  </div>
  </div>
  );
}
}

export default chat;
